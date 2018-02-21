from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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
                                        is_active=False)

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

