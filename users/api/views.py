"""
Module: users_api.views
Description: This module defines API views for user-related functionalities in the Users API app.
"""
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from blogs.api.permissions import IsCurrentUser

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserDetailUpdateSerializer,
)


class UserCreateAPIView(CreateAPIView):
    """
    API view for user registration.

    This view uses the UserCreateSerializer to handle user registration.
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(CreateAPIView):
    """
    API view for user login.

    This view uses the UserLoginSerializer to handle user login.
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user login.
        """
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """
    API view for user logout.

    This view logs out the user by deleting the JWT token cookie.
    """

    # pylint: disable=unused-argument
    def post(self, request):
        """
        Handle user logout.
        """
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "Message": "Successfully Logged Out"
        }
        return response


class UserDetailAPIView(RetrieveAPIView):
    """
    API view for retrieving user profile details.

    This view retrieves detailed information about a user's profile.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class UserDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view for updating user profile details.

    This view allows a user to update their profile information.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCurrentUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve user profile details.
        """
        try:
            instance = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
