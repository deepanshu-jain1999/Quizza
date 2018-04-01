from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from apps.serializers import SignupSerializer,\
                            LoginSerializer,\
                            ProfileSerializer,\
                            ChangePasswordSerializer,\
                            ForgetPasswordSerializer,\
                            SetPasswordSerializer, \
                            GetScoreSerializer
from django.contrib.auth.models import User
from apps.models import Profile, Category, Quiz, Score
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
            print("-----", str(self.request.user))

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


class ProfileList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)


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
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    # serializer_class = CategorySerializer

    def get(self, format=None):
        # print(self.request.data)
        cat = [cat.for_json() for cat in Category.objects.all()]
        print(json.dumps(cat))
        return Response(cat, status=status.HTTP_200_OK)


class Instruction(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

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
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    # serializer_class = CategorySerializer

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
        print("hello")
        serializer = self.serializer_class(data=self.request.data)
        print(serializer)

        if serializer.is_valid():
            print("111111")
            category = self.kwargs["category"]
            cat_obj = Category.objects.get(category=category)
            serializer.save(user=self.request.user, category=cat_obj)
            print("12222")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#     def get_queryset(self):
#         user = self.request.user
#         print("---->", user)
#         category = self.kwargs["category"]
#         print("---->", category)
#         cat_obj = Category.objects.get(category=category)
#         print("---->",cat_obj)
#         print(Score.objects.get(user=user, category=cat_obj))
#         return Score.objects.get(user=user, category=cat_obj)
#
#     def perform_create(self, serializer):
#         category = self.kwargs["category"]
#         cat_obj = Category.objects.get(category=category)
#         serializer.save(user=self.request.user, category=cat_obj)
#
#     def perform_update(self, serializer):
#         serializer.save()
#         # category = self.kwargs["category"]
#         # cat_obj = Category.objects.get(category=category)
#         # prev_score = Score.objects.get(user=self.request.user, category=cat_obj).score
#         # current_score = serializer.data["score"]
#         # if current_score>prev_score:
#         #     serializer.save(user=self.request.user, category=cat_obj, score=current_score)
#         # else:
#         #     serializer.save(user=self.request.user, category=cat_obj, score=prev_score)
#
#
# # def post(self, *args, **kwargs):
#     #     print("hello")
#     #     serializer = self.serializer_class(data=self.request.data)
#     #     print(serializer)
#     #
#     #     if serializer.is_valid():
#     #         print("111111")
#     #         category = self.kwargs["category"]
#     #         cat_obj = Category.objects.get(category=category)
#     #         serializer.save(user=self.request.user, category=cat_obj)
#     #         print("12222")
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             # category = self.kwargs["category"]
#             # cat_obj = Category.objects.get(category=category)
#             # current_score = serializer.data["score"]
#             # if Score.objects.filter(user=self.request.user, category=cat_obj).exists():
#             #
#             #     serializer.update()
#             #
#             # prev_score = Score.objects.get(user=self.request.user, category=cat_obj).score
