from .common import *

print("Connected to DEV")

# Only required for prod.
# ALLOWED_HOSTS = ['*']

DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e1iiz-og73%^z%cz3aklffj-$$ji9w+56fh(^usnt)1wsnk3d)'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }