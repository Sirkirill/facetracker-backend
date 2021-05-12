"""facein_api URL Configuration"""
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .admin import main_admin_site


urlpatterns = [
    path('api/profiles/', include('profiles.urls', namespace='profiles')),
    path('admin/', main_admin_site.urls),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns += [
    path('docs/', schema_view.with_ui(cache_timeout=0), name="documentation"),
]
