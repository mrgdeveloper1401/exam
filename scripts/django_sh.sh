#!/bin/sh

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
daphne async_django.asgi:application