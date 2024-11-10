FROM python:3.13-alpine3.20

RUN apk update
RUN apk upgrade --no-cache
RUN mkdir /PlayVault

WORKDIR /PlayVault

COPY .black.toml .black.toml
COPY .flake8 .flake8
COPY ./commands ./commands
COPY ./requirements.txt ./requirements.txt
COPY ./src ./src

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

CMD ["bin/sh"]