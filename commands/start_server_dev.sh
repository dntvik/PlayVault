#!/bin/sh

python src/manage.py test | flake8
python src/manage.py migrate
python src/manage.py check

python src/manage.py runserver 0:8000