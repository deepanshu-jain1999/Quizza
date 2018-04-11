from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from apps.models import Profile, Category, Score


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
    # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['profile_pic', 'name', 'city']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8)
    new_password = serializers.CharField(min_length=8)
    new_confirm_password = serializers.CharField(min_length=8)

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
        fields = ['category', 'cat_img']


class GetScoreSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', read_only=True)
    category = serializers.ReadOnlyField(source='category.category', read_only=True)

    class Meta:
        model = Score
        read_only_fields = ('user', 'category')
        fields = ['all_score', 'category', 'user']

    def create(self, validated_data):
        current_score = validated_data.get("all_score")
        cat_obj = validated_data.get("category")
        user = validated_data.get("user")
        level = validated_data.get("level")
        total_ques = validated_data.get("total_ques")
        obj, created = Score.objects.get_or_create(user=user, category=cat_obj)

        current_score = current_score/total_ques*100
        if level == "easy":
            prev_score = obj.easy_score
            if current_score > prev_score:
                obj.easy_score = current_score
        elif level == "medium":
            prev_score = obj.medium_score
            if current_score > prev_score:
                obj.medium_score = current_score
        elif level == "hard":
            prev_score = obj.hard_score
            if current_score > prev_score:
                obj.medium_score = current_score

        easy = obj.easy_score
        med = obj.medium_score
        hard = obj.hard_score
        total_score = (easy + med + hard)/3
        obj.all_score = total_score
        obj.save()
        return obj

