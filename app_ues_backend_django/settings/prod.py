from .common import *
import dj_database_url
DEBUG = False
SECRET_KEY = get_env('SECRET_KEY')

# Only required for prod.
# Change this if deployed somewhere else.
ALLOWED_HOSTS = ['app-ues-prod.herokuapp.com', 'localhost']

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': get_env('DB_NAME', 'backend'),
#             'USER': get_env('DB_USER', 'postgres'),
#             'PASSWORD': get_env('DB_PASSWORD', 'postgres'),
#             'HOST': get_env('DB_HOST', '192.168.0.11'),
#             'PORT': get_env('DB_PORT', '5432'),
#         }
#     }

DATABASES = {
    'default': dj_database_url.config()
}

print("Connected to PROD")