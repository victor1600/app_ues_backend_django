from .common import *
import dj_database_url
DEBUG = False
SECRET_KEY = get_env('SECRET_KEY')

# Only required for prod.
# Change this if deployed somewhere else.
ALLOWED_HOSTS = ['app-ues-prod.herokuapp.com', 'localhost']


DATABASES = {
    # This allows to get the database config from DATABASE_URL env var, and use
    # different type of db dynamically!
    'default': dj_database_url.config()
}

print("Connected to PROD")