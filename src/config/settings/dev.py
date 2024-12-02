import os

import mongoengine

from config.settings.base import *  # NOQA
from config.settings.base import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m%w$#lw&*t3w*@bj2l(92(p7aqubc0vl5z9(u)l!0mul^q-b6@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "localhost"]

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # NOQA

mongoengine.connect(host=os.environ.get("DJANGO_MONGO_CONNECTION"))

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT"),
        },
    }

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"  # NOQA
STATIC_URL = "static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # NOQA
MEDIA_URL = "media/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "media"),)
