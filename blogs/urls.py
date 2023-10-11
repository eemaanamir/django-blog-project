from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("bloglist/", views.blog_list_view, name="blog_list"),
    path("<int:blog_id>/blog/", views.single_blog_view, name="single_blog"),
    path("<int:user_id>/profile/", views.user_profile_view, name="user_profile"),
    path("subscribe/form/", views.sub_form_view, name="subscribe_form"),
    path("subscribe/plans/", views.sub_plans_view, name="subscribe_plans"),
    path("editprofile/", views.edit_profile_view, name="edit_profile"),
    path("<int:draft_id>/draft/edit/", views.edit_draft_view, name="edit_draft"),
    path("myblogs/<str:list_type>/", views.list_drafts_and_published, name="list_drafts_published"),
]