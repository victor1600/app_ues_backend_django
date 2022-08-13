#!/bin/sh

echo "Checking if data folder exists"
DIR="/app/media/"
if [ -d "$DIR" ]; then
  ### Take action if $DIR exists ###
  echo "media folder exists"
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Error: ${DIR} not found. Downloading..."
  ### Downloading media file from google drive
  wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1b_OHjSocfi-hsbASu2HHbpJWIdqPvASI' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1b_OHjSocfi-hsbASu2HHbpJWIdqPvASI" -O media.zip && rm -rf /tmp/cookies.txt
  unzip media.zip

fi

echo "performing migrations"
python3 manage.py makemigrations
python3 manage.py makemigrations user
python3 manage.py makemigrations api
python3 manage.py migrate


#
## populating db
#echo "Checking for new data"
#
#python app_ues_backend_django/load_data.py

echo "running server"

echo $DJANGO_SETTINGS_MODULE

if [ "$DJANGO_SETTINGS_MODULE" = "app_ues_backend_django.settings.prod" ]
then
  python3 manage.py collectstatic
  echo "Running app using PROD gunicorn server"
  gunicorn --bind 0.0.0.0:8000 app_ues_backend_django.wsgi
else
  echo "Running app using inbuilt DEV server"
  python3 manage.py runserver 0.0.0.0:8000
fi
