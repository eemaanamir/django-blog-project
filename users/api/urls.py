"""
Module: users_api.urls
Description: This module defines the URL patterns for the Users API app.
"""
from django.urls import path
from . views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserDetailAPIView,
    UserDetailUpdateAPIView,
)

# pylint: disable=invalid-name
app_name = 'users-api'

urlpatterns = [
    path("signup/", UserCreateAPIView.as_view(), name='signup'),
    path("login/", UserLoginAPIView.as_view(), name='login'),
    path("logout/", UserLogoutAPIView.as_view(), name='logout'),
    path("<int:pk>/profile/", UserDetailAPIView.as_view(), name='profile'),
    path("<int:pk>/profile/edit/", UserDetailUpdateAPIView.as_view(), name='edit_profile')
]
