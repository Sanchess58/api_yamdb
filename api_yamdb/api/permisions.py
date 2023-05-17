from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == "admin" or request.user.is_superuser)
        )


class IamOrReadOnly(permissions.BasePermission):
    """Собcтвенник или только чтение."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (obj == request.user)
