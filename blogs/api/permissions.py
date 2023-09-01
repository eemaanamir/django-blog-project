"""
Module: blog_api.permissions
Description: This module defines custom permission classes for the Blog API app.
"""
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
        Check if the user is the owner of a Blog.
        """
    message = 'You must be the owner of this Blog.'

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the Blog object.
        """
        return obj.user == request.user


class IsCurrentUser(BasePermission):
    """
   Check if the user is the owner of an Account.
   """
    message = 'You must be the owner of this Account.'

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the Account object.
        """
        return obj == request.user
