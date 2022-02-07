from .common import *
import dj_database_url

# TODO: Change this later.
DEBUG = False
SECRET_KEY = get_env('SECRET_KEY')
#

# Only required for prod.
# Change this if deployed somewhere else.
ALLOWED_HOSTS = ['*']


DATABASES = {
    # This allows to get the database config from DATABASE_URL env var, and use
    # different type of db dynamically!
    'default': dj_database_url.config()
}
