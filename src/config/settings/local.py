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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
