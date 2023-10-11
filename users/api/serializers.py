"""
Module: users_api.serializers
Description: This module defines serializers for user-related functionalities in the Users API app.
"""
import os
import numpy as np

from django.core.validators import MaxLengthValidator
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)
from rest_framework_simplejwt.tokens import RefreshToken

from emails import task
from users.models import User, Profile


class UserCreateSerializer(ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the validation and creation of new user accounts.
    """
    first_name = serializers.CharField(required=True,
                                       validators=[MaxLengthValidator(limit_value=150)])
    last_name = serializers.CharField(required=True,
                                      validators=[MaxLengthValidator(limit_value=150)])
    email = serializers.EmailField(required=True,
                                   validators=[MaxLengthValidator(limit_value=150)])
    password1 = serializers.CharField(write_only=True, label='Password',
                                      validators=[MaxLengthValidator(limit_value=150)])
    password2 = serializers.CharField(write_only=True, label='Confirm Password',
                                      validators=[MaxLengthValidator(limit_value=150)])
    user_bio = serializers.CharField(required=True, label='User Bio',
                                     validators=[MaxLengthValidator(limit_value=200)])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password1', 'password2', 'user_bio'
        ]

    def validate_password2(self, value):
        """
        Validate that the provided passwords match.

        This function ensures that the 'password1' and 'password2' fields match.
        """
        data = self.get_initial()
        password1 = data.get("password1")
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value

    def validate_email(self, value):
        """
        Validate that the provided email is unique.

        This function checks if the provided email is already in use by another user.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use."
                                  " Please use a different email.")
        return value

    def create(self, validated_data):
        """
        Create a new user account.

        This function creates a new User instance and associated Profile instance.
        """
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
        profile.user_otp = np.random.randint(100000, 999999)
        profile.save()

        task.send_mail_task.delay(user_obj.id)

        return validated_data


class ProfileDetailSerializer(ModelSerializer):
    """
    Serializer for Profile model to retrieve details.

    This serializer retrieves details about a user's profile.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
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
    """
    Serializer for User model to retrieve details.

    This serializer retrieves details about a user.
    """
    profile = ProfileDetailSerializer()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        ]


class UserLoginSerializer(ModelSerializer):
    """
    Serializer for user login.

    This serializer handles user login and generates JWT tokens.
    """
    token = serializers.CharField(allow_blank=True, read_only=True)
    refresh = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(label='Email Address', required=True)
    user = UserDetailSerializer(read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = User
        fields = [
            "user",
            "email",
            'password',
            "token",
            "refresh"
        ]
        extra_kwargs = {"password":
                            {"write_only": True},
                        }

    def validate(self, data):  # pylint: disable=arguments-renamed
        """
        Validate user login credentials and generate JWT tokens.

        This function validates the provided email and password, generates JWT tokens,
        and sets an HTTP-only cookie containing the token.
        """
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
        data["user"] = user_obj

        return data


class ProfileDetailUpdateSerializer(ModelSerializer):
    """
    Serializer for updating user profile details.

    This serializer handles updating user profile details.
    """
    user_bio = serializers.CharField(required=True, label='User Bio',
                                     validators=[MaxLengthValidator(limit_value=200)])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
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
            "user_dp": {"read_only": True}
        }


class UserDetailUpdateSerializer(ModelSerializer):
    """
    Serializer for updating user details.

    This serializer handles updating user details, including their profile information.
    """
    first_name = serializers.CharField(required=True,
                                       validators=[MaxLengthValidator(limit_value=150)])
    last_name = serializers.CharField(required=True,
                                      validators=[MaxLengthValidator(limit_value=150)])
    profile = ProfileDetailUpdateSerializer()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
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
            "email": {"read_only": True}}

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile_serializer = ProfileDetailUpdateSerializer(instance.profile,
                                                           data=profile_data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()

        return super().update(instance, validated_data)


class VerificationSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = Profile
        fields = ('username', 'otp')

