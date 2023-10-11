from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path("editprofile/", views.edit_profile_view, name="edit_profile"),
    path("editdp/", views.edit_dp_view, name="edit_dp"),
]