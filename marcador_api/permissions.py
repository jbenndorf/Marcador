from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user or request.user.is_superuser


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only supervisors to add or edit objects.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsPublicOrOwnerOrSuperuser(permissions.BasePermission):
    """
    Custom permission to allow only owners or superusers to edit
    an object.
    """

    def has_object_permission(self, request, view, obj):
        if obj.is_public or obj.owner == request.user or request.user.is_superuser:
            return True
