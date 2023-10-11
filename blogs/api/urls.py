from django.urls import path
from . views import *


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

