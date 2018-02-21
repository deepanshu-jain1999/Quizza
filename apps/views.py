from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.serializers import SignupSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from quizup.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string

class Signup(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                username = json["username"]
                email = json["email"]
                json['token'] = token.key
                msg_html = render_to_string('apps/email_content.html', {
                    'user': username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                subject = 'Activate your account'
                from_mail = EMAIL_HOST_USER
                message = 'hello how are you'
                to_mail = [email]
                send_mail(subject, message, from_mail, to_mail, fail_silently=False)
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

