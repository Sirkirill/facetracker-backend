from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PhotosConfig(AppConfig):
    name = 'photos'
    verbose_name = _('Photos')
