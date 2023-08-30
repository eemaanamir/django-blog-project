from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You must be the owner of this Blog.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCurrentUser(BasePermission):
    message = 'You must be the owner of this Account.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user

