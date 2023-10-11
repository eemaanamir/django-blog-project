from rest_framework.generics import (
    RetrieveDestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserDetailUpdateSerializer,
)

from users.models import User
from blogs.api.permissions import *


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "Message": "Successfully Logged Out"
        }
        return response


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class UserDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailUpdateSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCurrentUser]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


"""
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "123@123.com", "password": "onetwothree"}' \
  http://localhost:8000/api/token/


curl -H "Authorization: Bearer <access-token>
" http://127.0.0.1:8000/api/users/4/profile/


curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh-token>"}' \
  http://localhost:8000/api/token/refresh/
  
  
curl \
  -X PUT \
  -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzMzMxMzAyLCJpYXQiOjE2OTMzMjY3MzAsImp0aSI6IjA0ZDM4YmE4MTYwMzRjZTFhNDRhNGJjNDUyMzRlN2MwIiwidXNlcl9pZCI6NH0.VN4yqkTX-Imc02C4RGm3xH84nucf18yO1_NjkD5v1YY
  "\
  -d '{"blog_title":"new","blog_type":"basic","blog_topic":"none","blog_summary":"new","blog_content":"new","is_published":"True"}' \
  http://localhost:8000/api/blogs/8/edit/

"""
