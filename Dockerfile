FROM python:3.8.1-alpine

LABEL maintainer="Lev Lybin <lev.lybin@gmail.com>"

ARG APP_ENV
ARG DJANGO_COLLECTSTATIC
ARG DJANGO_MIGRATE
ARG START_SERVER

EXPOSE 5000 9001

ENV APP_ENV=${APP_ENV} \
    # https://docs.python.org/3.8/using/cmdline.html
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # https://github.com/pypa/pip/blob/master/src/pip/_internal/cli/cmdoptions.py
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # https://github.com/jwilder/dockerize
    DOCKERIZE_VERSION=v0.6.1 \
    # https://github.com/python-poetry/poetry
    POETRY_VERSION=1.0.2 \
    # https://github.com/benoitc/gunicorn
    GUNICORN_VERSION=20.0.4 \
    # https://github.com/Supervisor/supervisor
    SUPERVISOR_VERSION=4.1.0

# System deps:
RUN apk update \
    && apk upgrade \
    && apk add --no-cache \
    bash \
    pcre \
    libxml2 \
    mariadb-connector-c \
    tini \
    # https://pkgs.alpinelinux.org/packages?name=dockerize&branch=edge currently in testing
    && wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"

# Copy only requirements, to cache them in docker layer:
WORKDIR /pysetup
COPY ./poetry.lock ./pyproject.toml /pysetup/

# This is a special case. We need to run this script as an entry point:
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
COPY ./docker-cmd.sh /docker-cmd.sh
RUN chmod +x "/docker-entrypoint.sh" \
    && chmod +x "/docker-cmd.sh"

# Building system and app dependencies
RUN set -ex \
    && apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    mariadb-dev \
    libc-dev \
    musl-dev \
    pcre-dev \
    zlib-dev \
    jpeg-dev \
    libffi-dev \
    libxml2-dev \
    linux-headers \
    && pip install "poetry==$POETRY_VERSION" \
    && pip install "gunicorn==$GUNICORN_VERSION" \
    && pip install "supervisor==$SUPERVISOR_VERSION" \
    && poetry config virtualenvs.create false \
    && poetry install $(test "$APP_ENV" == production && echo "--no-dev") --no-interaction --no-ansi \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

WORKDIR /app
COPY . .

ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
CMD ["/docker-cmd.sh"]
