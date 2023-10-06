"""
Module: blogs.api.serializers
Description: This module contains serializer classes for the Blog API app.
"""

from django.core.validators import MaxLengthValidator
from django.urls import reverse
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField
)
from blogs.models import Blog
from users.api.serializers import UserDetailSerializer


class BlogListSerializer(ModelSerializer):
    """
    Serializer for listing blog posts with summarized information.
    """
    detail_url = HyperlinkedIdentityField(
        view_name='blog-api:detail',
        lookup_field='pk'
    )
    user_detail_url = SerializerMethodField()
    user = SerializerMethodField()
    blog_header_image = SerializerMethodField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = Blog
        fields = [
            'user',
            'user_detail_url',
            'id',
            'blog_header_image',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_date_time',
            'detail_url'
        ]

    def get_user(self, obj):
        """
        Get the full name of the user associated with the blog post.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The full name of the user.
        """
        return str(obj.user.first_name) + " " + str(obj.user.last_name)

    def get_user_detail_url(self, obj):
        """
        Get the URL to the user's profile associated with the blog post.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The URL to the user's profile.
        """
        user_instance = obj.user
        if user_instance:
            return self.context['request'].build_absolute_uri(
                reverse('users-api:profile', args=[user_instance.pk])
            )
        return None

    def get_blog_header_image(self, obj):
        """
        Get the blog header image URL.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The blog header image URL.
        """
        return obj.blog_header_image.url


class BlogDetailSerializer(ModelSerializer):
    """
    Serializer for detailed view of a single blog post.
    """
    user_detail_url = SerializerMethodField()
    blog_header_image = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = Blog
        fields = [
            'user',
            'user_detail_url',
            'id',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_content',
            'blog_date_time',
            'blog_likes_count',
            'blog_header_image'
        ]

    def get_user_detail_url(self, obj):
        """
        Get the URL to the user's profile associated with the blog post.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The URL to the user's profile.
        """
        user_instance = obj.user
        if user_instance:
            return self.context['request'].build_absolute_uri(
                reverse('users-api:profile', args=[user_instance.pk])
            )
        return None
    def get_blog_header_image(self, obj):
        """
        Get the blog header image URL.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The blog header image URL.
        """
        return obj.blog_header_image.url


class BlogDraftListSerializer(ModelSerializer):
    """
    Serializer for listing draft blog posts.
    """
    edit_url = HyperlinkedIdentityField(
        view_name='blog-api:edit',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='blog-api:delete',
        lookup_field='pk'
    )
    user = SerializerMethodField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = Blog
        fields = [
            'user',
            'id',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_date_time',
            'blog_header_image',
            'edit_url',
            'delete_url',
        ]

    def get_user(self, obj):
        """
        Get the full name of the user associated with the blog post.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The full name of the user.
        """
        return str(obj.user.first_name) + " " + str(obj.user.last_name)


class BlogPublishedListSerializer(ModelSerializer):
    """
    Serializer for listing published blog posts.
    """
    detail_url = HyperlinkedIdentityField(
        view_name='blog-api:detail',
        lookup_field='pk'
    )
    edit_url = HyperlinkedIdentityField(
        view_name='blog-api:edit',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='blog-api:delete',
        lookup_field='pk'
    )
    user = SerializerMethodField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = Blog
        fields = [
            'user',
            'id',
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_date_time',
            'blog_header_image',
            'detail_url',
            'edit_url',
            'delete_url'
        ]

    def get_user(self, obj):
        """
        Get the full name of the user associated with the blog post.
        Args:
            obj (Blog): The blog post instance.
        Returns:
            str: The full name of the user.
        """
        return str(obj.user.first_name) + " " + str(obj.user.last_name)


class BlogDraftCreateUpdateSerializer(ModelSerializer):
    """
    Serializer for creating and updating draft blog posts.
    """
    blog_title = serializers.CharField(required=True,
                                       validators=[MaxLengthValidator(limit_value=150)])
    blog_type = serializers.CharField(required=True)
    blog_topic = serializers.CharField(required=True)
    blog_summary = serializers.CharField(required=True,
                                         validators=[MaxLengthValidator(limit_value=200)])
    blog_content = serializers.CharField(required=True,
                                         validators=[MaxLengthValidator(limit_value=5000)])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass specifies the model and fields to include in the serializer.
        """
        model = Blog
        fields = [
            'blog_title',
            'blog_type',
            'blog_topic',
            'blog_summary',
            'blog_content',
            'is_published',
            'id',
        ]
        extra_kwargs = {
            "id": {"read_only": True}}

