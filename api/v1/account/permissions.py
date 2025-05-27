from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    message = "user authentication not access this view"

    def has_permission(self, request, view):
        return not request.user.is_authenticated
