from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.serializers import SignupSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth.models import User
from apps.models import Profile
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from quizup.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.views.generic import ListView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
# from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets


class Signup(APIView):
    """
    Creates the user.
    """
    serializer_class = SignupSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                username = json["username"]
                email = json["email"]
                current_site = get_current_site(request)

                self.email_send(self, user, username, email, current_site)
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def email_send(self,request, user, username, email, current_site):
        # current_site = get_current_site(request)
        message = 'hello how are you'
        msg_html = render_to_string('apps/email_template.html', {
            'user': username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),# add .decode() in django2+
            'token': account_activation_token.make_token(user),
        })
        subject = 'Activate your account'
        from_mail = EMAIL_HOST_USER
        to_mail = [email]

        return send_mail(subject,
                         message,
                         from_mail,
                         to_mail,
                         html_message=msg_html,
                         fail_silently=False
                         )


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
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            # login(request, user)
            return redirect('login')
        else:
            return HttpResponse("Invalid token")


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, format=None, **kwargs,):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print("-----", str(self.request.user))

            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProfileViewSet(viewsets.ModelViewSet):
    """
       This viewset automatically provides `list`, `create`, `retrieve`,
       `update` and `destroy` actions.
       Additionally we also provide an extra `highlight` action.
     """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
