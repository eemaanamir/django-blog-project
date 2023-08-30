from rest_framework.generics import (
    RetrieveDestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from .pagination import BlogPageNumberPagination
from blogs.models import Blog
from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer,
    BlogDraftCreateUpdateSerializer,
    BlogDraftListSerializer,
    BlogPublishedListSerializer
)
from .permissions import *


class BlogTimeLineListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = BlogPageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['blog_date_time', 'blog_likes_count']
    search_fields = ['blog_title', 'blog_type', 'blog_topic', 'blog_summary',
                     'blog_content', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailAPIView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BlogDraftListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDraftListSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = BlogPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user, is_published=False)


class BlogDraftCreateAPIView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDraftCreateUpdateSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogDraftUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDraftCreateUpdateSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


class BlogDraftDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


class BlogPublishedListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogPublishedListSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = BlogPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user, is_published=True)
