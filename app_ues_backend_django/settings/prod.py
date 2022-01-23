from .common import *

print("Connected to PROD")

DEBUG = truthiness(get_env('DEBUG', 'false'))
SECRET_KEY = get_env('SECRET_KEY')

# Only required for prod.
ALLOWED_HOSTS = ['*']

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_env('DB_NAME', 'backend'),
            'USER': get_env('DB_USER', 'doadmin'),
            'PASSWORD': get_env('DB_PASSWORD', 'phUQNbjqAQ8vPAAd'),
            'HOST': get_env('DB_HOST', 'db-mysql-nyc3-42223-do-user-7412275-0.b.db.ondigitalocean.com'),
            'PORT': get_env('DB_PORT', '25060'),
        }
    }
