#!/bin/sh

python src/manage.py migrate
python src/manage.py check
python src/manage.py loaddata admin_interface_theme_bootstrap.json
python src/manage.py collectstatic --noinput

#python src/manage.py runserver 0:8000

gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./src config.wsgi:application --log-level=${WSGI_LOG_LEVEL}