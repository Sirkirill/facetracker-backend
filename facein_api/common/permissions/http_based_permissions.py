from rest_framework.permissions import BasePermission


class HTTPMeta(type):
    """
    Metaclass which helps to create HTTP-based permissions for Django REST Framework.
    """
    def __getattr__(cls, method):
        class Method(BasePermission):
            message = 'HTTP method is not allowed.'

            def has_permission(self, request, view):
                return request.method == method.upper()

            def has_object_permission(self, request, view, obj):
                return self.has_permission(request, view)

        return Method


class HTTP(metaclass=HTTPMeta):
    """
    Permission class which is used as a HTTP-based Django REST Permission Class based
    on rest_framework.permissions.BasePermission.

    Example:
        HTTP.GET - can be used as a permission class which indicates that GET request is made.
        HTTP.patch - any string can be used, name of http method is case-insensitive.
    """
    pass
