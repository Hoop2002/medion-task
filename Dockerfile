FROM python:3.11.10-alpine AS build

RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/app \
    APP_HOME=/home/app/web \
    #POETRY CONFIG
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.4

RUN mkdir ${APP_HOME} && mkdir ${APP_HOME}/staticfiles && mkdir ${APP_HOME}/mediafiles
WORKDIR ${APP_HOME}
RUN chown -R app:app ${HOME}

RUN apk update && apk add bash && apk add curl
RUN curl -sSL https://install.python-poetry.org | python -
COPY . ${APP_HOME}
RUN poetry install

USER app