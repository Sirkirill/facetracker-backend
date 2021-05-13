# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
import dj_database_url
from decouple import config


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    ),
}
