from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name='home'),
    path('login/', views.login_view, name='login'),
    path("editprofile/", views.edit_profile_view, name="edit_profile"),
]