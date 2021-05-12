from rest_framework.permissions import BasePermission


class ActionMeta(type):
    """
    Metaclass which helps to create Action-based permissions for Django REST Framework viewsets.
    """
    def __getattr__(cls, action):
        class ActionPermission(BasePermission):
            message = 'Action is not allowed.'

            def has_permission(self, request, view):
                return view.action == action.lower()

            def has_object_permission(self, request, view, obj):
                return self.has_permission(request, view)

        return ActionPermission


class Action(metaclass=ActionMeta):
    """
    Permission class which is used as a Action-based Django REST Permission Class based
    on rest_framework.permissions.BasePermission which is created for viewsets.

    Example:
        ACTION.list - can be used as a permission class which indicates that list request
        for viewset is made.
        ACTION.VIEW - any string can be used, name of http method is case-insensitive.
    """
    pass
