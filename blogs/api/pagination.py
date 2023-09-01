"""
Module: blog_api.pagination
Description: This module defines custom pagination classes for the Blog API app.
"""
from rest_framework.pagination import PageNumberPagination


class BlogPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class for controlling blog post listing pages.
    """

    page_size = 2
