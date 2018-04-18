from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from apps.models import Category, Profile, EasyInstruction, MediumInstruction, HardInstruction
from rest_framework.authtoken.models import Token


class UserSignupTest(APITestCase):
    url = reverse('signup')

    def test_create_user(self):
        data = {'username': 'any_username', 'email': 'xyz@gmail.com', 'password': 'any_password'}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_email_require(self):
        data = {'username': 'any_username', 'email': '', 'password': 'any_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        data = {'username': 'any_username', 'password': 'any_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_require(self):
        data = {'username': 'any_username', 'email': 'xyz@gmail.com', 'password': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        data = {'username': 'any_username', 'email': 'xyz@gmail.com',}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_username_require(self):
        data = {'username': '', 'email': 'xyz@gmail.com', 'password': 'password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        data = {'email': 'xyz@gmail.com', 'password': 'password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_email_unique(self):
        data = {'username': 'anyusername1', 'email': 'xyz1@gmail.com', 'password': 'password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        data = {'username': 'anyusername2', 'email': 'xyz1@gmail.com', 'password': 'password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data["email"][0], "This field must be unique.")


class UserLoginTest(APITestCase):
    url = reverse("login")

    # def test_login_authentication(self):
    #     user = User.objects.create(username='username',
    #                                     password='password',
    #                                     email='xyz@gmail.com'
    #                                     )
    #
    #     # token = Token.objects.create(user=user)
    #     user.is_active = True
    #     Profile.objects.create(user=user)
    #     # user.save()
    #     data = {'username': 'username', 'password': 'password'}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['token'], user.auth_token.key)

    def test_login_user_failing(self):
        user = User.objects.create(username='username',
                                        password='password',
                                        email='xyz@gmail.com')
        token = Token.objects.create(user=user)
        data = {'username': 'username', 'password': 'wrong_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('token' in response.data, False)


class UserProfileTest(APITestCase):
    url = reverse("profile")

    def test_Userprofile_default(self):
        user = User.objects.create(username='username',
                                   password='password',
                                   email='xyz@gmail.com')
        Profile.objects.create(user=user)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], None)
        self.assertEqual(response.data['city'], None)
        self.assertEqual(len(response.data), 4)

    def test_user_profile_after_edit(self):
        user = User.objects.create(username='username',
                                   password='password',
                                   email='xyz@gmail.com')
        Profile.objects.create(user=user)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
        data = {"name": "my_name"}
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "my_name")
        self.assertEqual(response.data['city'], None)
        self.assertEqual(len(response.data), 3)


class CheckAllCategoryTest(APITestCase):
    url = reverse("category_list")

    def test_check_all_category(self):
        user = User.objects.create(username='username',
                                      password='password',
                                      email='xyz@gmail.com',
                                      is_active=True)

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))

        obj1 = EasyInstruction.objects.get_or_create(instr="123")[0]
        obj2 = MediumInstruction.objects.get_or_create(instr="123")[0]
        obj3 = HardInstruction.objects.get_or_create(instr="123")[0]
        Category.objects.create(category="science",
                                )
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["category"], "science")

# class ChangePasswordTest(APITestCase):
#     url = reverse("change-password")
#
#     def test_by_change_password(self):
#         user = User.objects.create(username='username',
#                                    password='password',
#                                    email='xyz@gmail.com',
#                                    is_active=True)
#
#         token = Token.objects.create(user=user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
#         self.client.force_login(user=user)
#         data = {"old_password": "password", "new_password": "123pass123", "new_conf_pass": "123pass123"}
#         response = self.client.post(self.url, data)
#         print("res->", response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['message'], "password has been changed")
#         self.assertEqual(len(response.data), 1)
#
#


