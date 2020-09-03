#! /usr/bin/env sh
set -e

# Start Gunicorn
exec gunicorn \
    -c gunicorn_conf.py \
    books.wsgi:application
