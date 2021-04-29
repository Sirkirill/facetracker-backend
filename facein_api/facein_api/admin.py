from django.contrib.admin import AdminSite


class MainAdminSite(AdminSite):
    """
    Admin Panel for FaceIn admins(superusers).
    """
    site_header = "Main Admin Site"
    site_title = "Main Admin Site"
    index_title = "Main Admin Site"

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_superuser


main_admin_site = MainAdminSite(name='main_admin')
