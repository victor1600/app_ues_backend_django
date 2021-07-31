#!/bin/sh

echo "performing migrations"
python manage.py makemigrations api
python manage.py migrate

echo "running server"
python manage.py runserver 0.0.0.0:8000