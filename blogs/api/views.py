"""
Module: blog_api.views
Description: This module defines API views for handling blog posts in the Blog API app.
"""
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
from blogs.models import Blog
from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer,
    BlogDraftCreateUpdateSerializer,
    BlogDraftListSerializer,
    BlogPublishedListSerializer
)
from .permissions import IsOwner
from .pagination import BlogPageNumberPagination


class BlogTimeLineListAPIView(ListAPIView):
    """
    API view for listing blog posts in a timeline.

    This view lists all published blog posts in a timeline format.
    Users can search for posts and order them by date and likes count.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = BlogPageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['blog_date_time', 'blog_likes_count']
    search_fields = ['blog_title', 'blog_type', 'blog_topic', 'blog_summary',
                     'blog_content', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        """
        Get the queryset of published blog posts for the timeline.

        Returns:
            QuerySet: The queryset of published blog posts.
        """
        return Blog.objects.filter(is_published=True)


class BlogDetailAPIView(RetrieveAPIView):
    """
    API view for retrieving a detailed blog post.

    This view retrieves a detailed representation of a single blog post.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BlogDraftListAPIView(ListAPIView):
    """
    API view for listing draft blog posts.

    This view lists all draft blog posts created by the authenticated user.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogDraftListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = BlogPageNumberPagination

    def get_queryset(self):
        """
         Get the queryset of draft blog posts for the authenticated user.

         Returns:
             QuerySet: The queryset of draft blog posts.
         """
        user = self.request.user
        return Blog.objects.filter(user=user, is_published=False)


class BlogDraftCreateAPIView(CreateAPIView):
    """
    API view for creating a draft blog post.

    This view allows authenticated users to create new draft blog posts.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogDraftCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Perform the creation of a new draft blog post.

        Args:
            serializer (BlogDraftCreateUpdateSerializer): The serializer instance.
        """
        serializer.save(user=self.request.user)


class BlogDraftUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view for updating a draft blog post.

    This view allows authenticated users to update their own draft blog posts.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogDraftCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


class BlogDraftDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view for deleting a draft blog post.

    This view allows authenticated users to delete their own draft blog posts.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


class BlogPublishedListAPIView(ListAPIView):
    """
    API view for listing published blog posts of the authenticated user.

    This view lists all published blog posts created by the authenticated user.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogPublishedListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = BlogPageNumberPagination

    def get_queryset(self):
        """
        Get the queryset of published blog posts for the authenticated user.

        Returns:
            QuerySet: The queryset of published blog posts.
        """
        user = self.request.user
        return Blog.objects.filter(user=user, is_published=True)
