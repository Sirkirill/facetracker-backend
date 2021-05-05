"""facein_api URL Configuration"""
from django.urls import include
from django.urls import path

from rest_framework import routers
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response

from profiles.models import User
from views import LoginView
from .admin import main_admin_site
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', main_admin_site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
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
   permission_classes=(permissions.AllowAny, )
)


urlpatterns += [
    path('docs/', schema_view.with_ui(cache_timeout=0), name="documentation"),
]

