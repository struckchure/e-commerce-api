#! /bin/sh

set -e


python manage.py migrate --noinput

DEFAULT_PORT=8000
PORT=${PORT:-$DEFAULT_PORT}

gunicorn e_commerce.wsgi --bind 0.0.0.0:$PORT
