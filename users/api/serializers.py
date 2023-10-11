import datetime
import jwt
from django.core.validators import MaxLengthValidator
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)

from users.models import User, Profile
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True, validators=[MaxLengthValidator(limit_value=150)])
    last_name = serializers.CharField(required=True, validators=[MaxLengthValidator(limit_value=150)])
    email = serializers.EmailField(required=True, validators=[MaxLengthValidator(limit_value=150)])
    password1 = serializers.CharField(write_only=True, label='Password',
                                      validators=[MaxLengthValidator(limit_value=150)])
    password2 = serializers.CharField(write_only=True, label='Confirm Password',
                                      validators=[MaxLengthValidator(limit_value=150)])
    user_bio = serializers.CharField(required=True, label='User Bio',
                                     validators=[MaxLengthValidator(limit_value=200)])

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password1', 'password2', 'user_bio'
        ]

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password1")
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use."
                                  " Please use a different email.")
        return value

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password1']

        user_obj = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user_obj.set_password(password)
        user_obj.save()

        profile = Profile.objects.get(user=user_obj)
        profile.user_bio = validated_data['user_bio']
        profile.save()

        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    refresh = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(label='Email Address', required=True)

    class Meta:
        model = User
        fields = [
            "email",
            'password',
            "token",
            "refresh"
        ]
        extra_kwargs = {"password":
                            {"write_only": True}}

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        user = User.objects.filter(username=email)
        if user.exists():
            user_obj = user.first()
        else:
            raise ValidationError("This Email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again.")

        refresh = RefreshToken.for_user(user_obj)
        token = str(refresh.access_token)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        data["token"] = token
        data["refresh"] = refresh

        return data


class ProfileDetailSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user_bio',
            'has_credit_card',
            'user_type',
            'user_dp',
            'blog_count',
            'likes',
            'followers'
        ]


class UserDetailSerializer(ModelSerializer):
    profile = ProfileDetailSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        ]


class ProfileDetailUpdateSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user_bio',
            'has_credit_card',
            'user_type',
            'user_dp',
            'blog_count',
            'likes',
            'followers'
        ]
        extra_kwargs = {
            "has_credit_card": {"read_only": True},
            "user_type": {"read_only": True},
            "blog_count": {"read_only": True},
            "likes": {"read_only": True},
            "followers": {"read_only": True},
        }


class UserDetailUpdateSerializer(ModelSerializer):
    profile = ProfileDetailUpdateSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
            "email": {"read_only": True}
        }
