from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.serializers import SignupSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from quizup.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.views.generic import ListView
from django.contrib.auth.views import login
from django.shortcuts import render, redirect, reverse
from django.http import Http404


class Signup(APIView):
    """
    Creates the user.
    """
    def post(self, request, format='json'):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                print("--->",user)
                token = Token.objects.create(user=user)
                print("tokin1",token)
                json = serializer.data
                username = json["username"]
                email = json["email"]
                # current_user = User.objects.get(username=username)
                # current_user.is_active = False
                # current_user.save()
                json['token'] = token.key
                current_site = get_current_site(request)

                message = 'hello how are you'
                msg_html = render_to_string('apps/email_template.html', {
                    'user': username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                subject = 'Activate your account'
                from_mail = EMAIL_HOST_USER
                to_mail = [email]
                send_mail(subject, message, from_mail, to_mail, html_message=msg_html, fail_silently=False)
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activate(ListView):
    def get(self, request, *args, **kwargs):
        try:
            x = self.kwargs['uidb64']
            # decode the uid from 64 base to normal text
            uid = force_text(urlsafe_base64_decode(x))
            # fetch user information
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print("------>", user)
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return Http404


class Login(APIView):
    pass