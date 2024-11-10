FROM python:3.12.7-alpine3.20

RUN apk update
RUN apk upgrade --no-cache
RUN mkdir /playvault

WORKDIR /playvault

COPY .black.toml .black.toml
COPY .flake8 .flake8
COPY ./requirements.txt ./requirements.txt
COPY ./commands ./commands
RUN mkdir -p /root/.cache/pip
COPY ./src ./src

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt
CMD ["bin/sh"]