from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from apps.serializers import SignupSerializer,\
                            LoginSerializer,\
                            ProfileSerializer,\
                            ChangePasswordSerializer,\
                            ForgetPasswordSerializer,\
                            SetPasswordSerializer, \
                            GetScoreSerializer, CategorySerializer
from django.contrib.auth.models import User
from apps.models import Profile, Category, Quiz, Score, CompeteQuiz
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from quizup.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from rest_framework import permissions, generics
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.core import serializers
import json


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
                text = "Please Activate Your Account By clicking below :"
                button = "Activate"
                email_send(user, username, email, current_site, button, text)
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def email_send(user, username, email, current_site, button, text):
    message = 'hello how are you'
    msg_html = render_to_string('apps/email_template.html', {
        'user': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),        # add .decode() in django2+
        'token': account_activation_token.make_token(user),
        'button': button,
        'text': text,
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
            Profile.objects.create(user=user)
            user.save()
            # login(request, user)
            return redirect('http://localhost:4200/welcome')
        else:
            return HttpResponse("Invalid token")


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, format=None, **kwargs,):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# class ProfileViewSet(viewsets.ModelViewSet):
#     """
#        This viewset automatically provides `list`, `create`, `retrieve`,
#        `update` and `destroy` actions.
#        Additionally we also provide an extra `highlight` action.
#      """
#
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = ProfileSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return Profile.objects.filter(user=user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class UserProfile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        queryset = Profile.objects.get(user=self.request.user)
        serializer = self.serializer_class(queryset, context={"request": request})
        data = serializer.data
        score = Score.objects.filter(user=self.request.user)
        score_dic = {}
        for obj in score:
            cat_name = obj.category.category
            score = obj.score
            score_dic[cat_name] = score
        print(score_dic)
        cat_with_score = {"category": [score_dic]}
        data.update(cat_with_score)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, format=None, **kwargs, ):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = authenticate(username=self.request.user.username, password=old_password)
            if user:
                user = self.request.user
                user.set_password(new_password)
                user.save()
                return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ForgetPassword(APIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, format=None, **kwargs,):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            if user:
                current_site = get_current_site(self.request)
                text = " Change your account password on click below:"
                button = "Change here"
                email_send(user, user.username, email, current_site, button, text)
                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeForgetPassword(ListView):

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

            # login(request, user)
            return redirect('http://localhost:4200/forget_password')
        else:
            return HttpResponse("Invalid token")


class SetPassword(APIView):
    serializer_class = SetPasswordSerializer

    def post(self, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            pass


class CategoryList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CategorySerializer

    def get(self, format=None):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={"request": self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class Instruction(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):
        category = self.kwargs["category"]
        level = self.kwargs["level"]
        cat = Category.objects.get(category=category)
        count = Quiz.objects.filter(category=cat, level=level).count()
        inst = []
        time = 20
        if level == "easy":
            time = cat.time_per_ques_easy
            inst = [obj.instr for obj in cat.easy_instr.all()]

        elif level == "medium":
            time = cat.time_per_ques_medium
            inst = [obj.instr for obj in cat.medium_instr.all()]

        elif level == "hard":
            time = cat.time_per_ques_hard
            inst = [obj.instr for obj in cat.hard_instr.all()]
        json_obj = dict(count=count, time_per_ques=time, instruction=inst)
        return Response(json_obj, status=status.HTTP_200_OK)


class PlayQuiz(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CategorySerializer

    def get(self, *args, **kwargs):
        category = self.kwargs["category"]
        level = self.kwargs["level"]
        no = int(self.kwargs["pk"])-1
        cat = Category.objects.get(category=category)
        quiz = Quiz.objects.filter(category=cat, level=level)[no]
        quiz = quiz.for_json()
        return Response(quiz, status=status.HTTP_200_OK)


class GetScore(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetScoreSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        print(serializer)

        if serializer.is_valid():
            category = self.kwargs["category"]
            cat_obj = Category.objects.get(category=category)
            serializer.save(user=self.request.user, category=cat_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompeteQuizView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = CategorySerializer

    def get(self, *args, **kwargs):
        category = self.kwargs["category"]
        cat = Category.objects.get(category=category)
        quiz = CompeteQuiz.objects.filter(category=cat)
        quiz = [quiz_obj.for_json() for quiz_obj in quiz]
        return Response(quiz, status=status.HTTP_200_OK)

