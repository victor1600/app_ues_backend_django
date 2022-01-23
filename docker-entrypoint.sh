#!/bin/sh

echo "performing migrations"
python manage.py makemigrations api
python manage.py makemigrations users
python manage.py migrate

echo "running server"
# for dev
python manage.py runserver 0.0.0.0:8000

# for prod, added 0.0.0.0:8000 for running it local inside docker.
# gunicorn --bind 0.0.0.0:8000 app_ues_backend_django.wsgi