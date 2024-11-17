FROM python:3.12.7-alpine3.20

RUN apk update
RUN apk upgrade --no-cache
RUN mkdir /playvault

WORKDIR /playvault

COPY .black.toml .black.toml
COPY .flake8 .flake8
COPY ./commands ./commands
COPY ./requirements.in ./requirements.in
COPY ./src ./src

RUN python -m pip install --upgrade pip pip-tools && pip-compile --upgrade && pip-sync

CMD ["bin/sh"]