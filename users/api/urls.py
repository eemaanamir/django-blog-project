from django.urls import path
from . views import *


app_name = 'users-api'

urlpatterns = [
    path("signup/", UserCreateAPIView.as_view(), name='signup'),
    path("login/", UserLoginAPIView.as_view(), name='login'),
    path("logout/", UserLogoutAPIView.as_view(), name='logout'),
    path("<int:pk>/profile/", UserDetailAPIView.as_view(), name='profile'),
    path("<int:pk>/profile/edit/", UserDetailUpdateAPIView.as_view(), name='edit_profile')
]