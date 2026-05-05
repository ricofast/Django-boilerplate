from rest_framework.permissions import BasePermission


class IsSelfOrRoleAdmin(BasePermission):
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        owner = getattr(obj, "user", obj)
        return owner == user or getattr(user, "is_role_admin", False)


class IsRoleAdmin(BasePermission):
    message = "Admin role required."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_role_admin", False))
