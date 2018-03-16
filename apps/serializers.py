from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from apps.models import Profile, Category


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(max_length=100,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'],
                                        # is_active=False,
                                        )
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        print("-->", attrs)

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    message = "Not authenticate user"
                    raise serializers.ValidationError(message)

            else:
                message = "Not matching username and password"
                raise serializers.ValidationError(message)

        else:
            message = 'Include both username and  password'
            raise serializers.ValidationError(message,)

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['name', 'city', 'profile_pic', 'user']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8)
    new_password = serializers.CharField(min_length=8)
    new_confirm_password = serializers.CharField(min_length=8)

    class Meta:

        def validate(self, attrs):
            old_password = attrs.get('old_password')
            new_password = attrs.get('new_password')
            new_confirm_password = attrs.get('new_confirm_password')

            if new_password != new_confirm_password:
                message = "Enter the same password"
                raise serializers.ValidationError(message)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(min_length=8)


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
    new_confirm_password = serializers.CharField(min_length=8)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category']

