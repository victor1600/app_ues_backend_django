#!/bin/bash

echo "Checking if data folder exists"
DIR="/app/media/"
if [ -d "$DIR" ]; then
  ### Take action if $DIR exists ###
  echo "media folder exists"
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Error: ${DIR} not found. Downloading..."
  wget https://victor-g95-2.s3.amazonaws.com/media.zip
  unzip media.zip
fi

echo "performing migrations"
python manage.py makemigrations
python manage.py makemigrations user
python manage.py makemigrations api
python manage.py migrate


#
## populating db
#echo "Checking for new data"

#python app_ues_backend_django/load_data.py

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
