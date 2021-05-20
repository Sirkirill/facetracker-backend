# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

from django.utils.translation import gettext_lazy as _
import os

from settings.django import BASE_DIR

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uk', _('Ukrainian')),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
