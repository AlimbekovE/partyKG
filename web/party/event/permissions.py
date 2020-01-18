from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrbjectIsPersonal(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_staff or
            obj.is_personal == True and obj.owner == request.user
        )
