#!/bin/sh

python src/manage.py migrate
python src/manage.py check
python src/manage.py loaddata admin_interface_theme_bootstrap.json
python src/manage.py collectstatic --noinput --clear

python src/manage.py runserver 0:8000