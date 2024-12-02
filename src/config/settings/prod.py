import os

import mongoengine

from config.settings.base import *  # NOQA
from config.settings.base import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "ec2-13-53-187-117.eu-north-1.compute.amazonaws.com"]

mongoengine.connect(host=os.environ.get("DJANGO_MONGO_CONNECTION"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"  # NOQA
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # NOQA
MEDIA_URL = "/media/"
