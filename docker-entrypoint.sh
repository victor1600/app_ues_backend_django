#!/bin/bash

echo "performing migrations"
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate

echo "running server"

echo $DJANGO_SETTINGS_MODULE

if [ "$DJANGO_SETTINGS_MODULE" = "app_ues_backend_django.settings.prod" ]
then
  python manage.py collectstatic
  echo "Running app using PROD gunicorn server"
  gunicorn --bind 0.0.0.0:8000 app_ues_backend_django.wsgi
else
  echo "Running app using inbuilt DEV server"
  python manage.py runserver 0.0.0.0:8000
fi
