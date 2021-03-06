from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsObjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            obj.owner == request.user
        )


class IsPostImageOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user and request.user.is_authenticated and
                obj.post.owner == request.user) or \
               request.user.is_staff


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            obj == request.user
        )


class IsObjectUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            obj.user == request.user
        )
