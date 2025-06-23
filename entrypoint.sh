#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata initial_data.json || true
# Start the Gunicorn server
# Ensure the environment is set up correctly



exec gunicorn titanic_project.wsgi:application --bind 0.0.0.0:80

