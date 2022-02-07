#!/bin/bash

echo "performing migrations"
python manage.py makemigrations
python manage.py makemigrations api
python manage.py makemigrations users
python manage.py migrate
python manage.py collectstatic

echo "running server"
# for dev
# python manage.py runserver 0.0.0.0:8000

echo $DJANGO_SETTINGS_MODULE

if [ "$DJANGO_SETTINGS_MODULE" = "app_ues_backend_django.settings.prod" ]
then
  echo "Running app using PROD gunicorn server"
  gunicorn --bind 0.0.0.0:8000 app_ues_backend_django.wsgi
else
  echo "Running app using inbuilt DEV server"
  python manage.py runserver 0.0.0.0:8000
fi

# for prod, added 0.0.0.0:8000 for running it local inside docker.
#gunicorn --bind 0.0.0.0:8000 app_ues_backend_django.wsgi