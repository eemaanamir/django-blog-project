"""
Module: blog_api.urls
Description: This module defines the URL patterns for the Blog API app.

App Namespace: 'blog-api'
"""
from django.urls import path
from . views import (
    BlogTimeLineListAPIView,
    BlogDraftListAPIView,
    BlogPublishedListAPIView,
    BlogDetailAPIView,
    BlogDraftUpdateAPIView,
    BlogDraftDeleteAPIView,
    BlogDraftCreateAPIView
)

# pylint: disable=invalid-name
app_name = 'blog-api'

urlpatterns = [
    path("list/", BlogTimeLineListAPIView.as_view(), name='list'),
    path("drafts/", BlogDraftListAPIView.as_view(), name='drafts'),
    path("published/", BlogPublishedListAPIView.as_view(), name='published'),
    path("<int:pk>/detail/", BlogDetailAPIView.as_view(), name='detail'),
    path("<int:pk>/edit/", BlogDraftUpdateAPIView.as_view(), name='edit'),
    path("<int:pk>/delete/", BlogDraftDeleteAPIView.as_view(), name='delete'),
    path("create/", BlogDraftCreateAPIView.as_view(), name='create'),
]
