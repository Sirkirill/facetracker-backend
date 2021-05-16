from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class MainAdminSite(AdminSite):
    """
    Admin Panel for FaceIn admins(superusers).
    """
    site_header = _("Main Admin Panel")
    site_title = _("Main Admin Panel")
    index_title = _("Main Admin Panel")

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_superuser


class ClientAdminSite(AdminSite):
    """
    Admin Panel for FaceIn client admins.
    """
    site_header = _("Admin Panel")
    site_title = _("Admin Panel")
    index_title = _("Admin Panel")

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and (request.user.is_admin or request.user.is_superuser)


main_admin_site = MainAdminSite(name='main_admin')
admin_site = ClientAdminSite(name='admin')
