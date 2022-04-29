#!/bin/bash

echo "performing migrations"
python manage.py makemigrations
python manage.py makemigrations user
python manage.py makemigrations api
python manage.py migrate

echo "Checking if data folder exists"
DIR="/app/data/"
if [ -d "$DIR" ]; then
  ### Take action if $DIR exists ###
  echo "data folder exists"
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Error: ${DIR} not found. Downloading..."
  #wget https://victor95-files.s3.amazonaws.com/data.zip
  #wget https://victor-g95-2.s3.amazonaws.com/data.zip
  wget --no-check-certificate --no-proxy "https://victor-g95-2.s3.us-east-1.amazonaws.com/data.zip?response-content-disposition=attachment&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDkaCXVzLWVhc3QtMSJHMEUCIQDbkYsCohKpdLtTYk7n%2FYi0UfeHGwJvnEf%2B%2FmcSQ5%2F58gIgM2PebmUSnFfvUKhAhG%2FG9HMgiuomh6aq3z2qAprD4BQq7QII8v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwwNTYwNTY5NTM5ODAiDE0fNIYHzptksF6a5CrBAmNE8wMF38tTc%2B2Or4BaVTd8lv8t7yjoW9LqvcNXQ%2FF9tq910ESSJWJBz7jQYBFXo6i9FchWydr%2F53K%2FQyHeIKiWgbMGZbii%2FFnPS1Fr%2BpOKc8lEZfxNyfW38ReZ0fS%2FDbSgGNPr68%2BPA7TgZY7D3RsdaKaTu4T02fGv8MJozmfXnq0hqm%2BNDo7z4KlHVvdAHIVL%2Fa18y5yQ%2FsDRwRx8Tm9rASQlFjX7VapoUADvMyzEWtmGFXsxCURi0SN8XmcVLuZp4nMksr3vPOEgMQssVaxWFkJZI%2Fglf9hK%2FjBkVm00PJfYsz9D7O%2BYOGhC%2F29zeFs9ackvZ5BaUTI8MA2Lb8OIWBQOq8%2F5PzAdnx%2BxWRkrOuCn8z8%2BmdDMJ9IR7toVIZjA31a2vnZoWw4KijhPqXtG6PSSfIpKbO2LHbzIPlbaoTCKkrCTBjqzAk3vsDrZc0g8bE6Fy5dCJMRcBkr79FPIPc7JSF3ZnTIspsHaq89ebv0o5kJKgwwdYPLReVuLtN0d0psE4RYOGjp1Mi%2FGJkBG3tx69P80%2FvTK%2BgEAhBVaq%2Fv%2FMlklAELawW%2BB%2BeDjwlJ7RdM0QwKB3j98c5YRXuWZEMKSZ2PAzoBvTFwFZWVgMZfb8A%2ByDIYGLf4MzO2rr7qiothB6lD3oKcXTOy1CZPuXQZMJYhdZewbn%2Bjom6WzOQNKTuPGJL7qMeYTdQpeyBZLgAjzCIA17a%2BlCZLZ0UF3sI1pXd9XknoY%2BMoL5JtqaPf8k5LcG%2FFc6ukyC4F%2Bb6MBaE2Guf93EA2cjugs72pFg3zagYUhTJT5Xv%2ByXeGhY7grs45RbWD5EjHn92ktCCSBXzIwxLuOHXr%2FNgQ%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220429T163023Z&X-Amz-SignedHeaders=host&X-Amz-Expires=299&X-Amz-Credential=ASIAQ2DKBHR6BJA3SOEJ%2F20220429%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e570f2a7765e7c4005894dfd0999cbcdfbb5414830ed30cc3b6ccb4e0b292955"
  unzip data.zip
fi

# populating db
echo "Checking for new data"
python app_ues_backend_django/load_data.py

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
