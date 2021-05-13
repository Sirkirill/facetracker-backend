from rest_framework.permissions import BasePermission

from profiles.models import User


class IsSuperUser(BasePermission):
    """
    Allows access only for superusers.
    """
    message = 'User is not a superuser.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdmin(BasePermission):
    """
    Allows access only for admins.

    Object permission checks that object is from the same company where user is an admin.
    """
    message = 'User is not an admin of the company.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        if isinstance(obj, User):
            return obj.company_id == request.user.company_id
        return False


class IsSecurityGuide(BasePermission):
    """
    Allows access only for securities.

    Object permission checks that object is from the same company where user is an security.
    """
    message = 'User is not a security guide.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_security

    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        if isinstance(obj, User):
            return obj.company_id == request.user.company_id
        return False


class IsSameCompany(BasePermission):
    """
    Allow access only for users from the same company.
    """
    message = 'User is not able to access data about other companies.'

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if isinstance(obj, User):
            return request.user.company_id == obj.company_id
        return False


class IsOwner(BasePermission):
    """
    Allow access only for owner of resource.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user == obj
        return False
