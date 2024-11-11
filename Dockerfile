FROM python:3.13-alpine3.20

RUN apk update
RUN apk upgrade --no-cache
RUN mkdir /PlayVault

WORKDIR /PlayVault

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./commands ./commands

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt
CMD ["./commands/start_server_dev.sh"]