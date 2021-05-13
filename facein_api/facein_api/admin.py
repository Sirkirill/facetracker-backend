from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class MainAdminSite(AdminSite):
    """
    Admin Panel for FaceIn admins(superusers).
    """
    site_header = _("FaceIn Admin")
    site_title = _("FaceIn Admin")
    index_title = _("FaceIn Admin")

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_superuser


main_admin_site = MainAdminSite(name='main_admin')
