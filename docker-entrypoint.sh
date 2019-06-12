#!/usr/bin/env bash

set -e

if [[ ! -z "$DB_DEFAULT_HOST" ]]; then
    echo "Wait until DB_DEFAULT is definitely ready"
    ./wait-for-it.sh "$DB_DEFAULT_HOST:$DB_DEFAULT_PORT" -- echo "DB_DEFAULT is up - continuing"
fi

if [[ ! -z "$DB_JAVA_WALLET_HOST" ]]; then
    echo "Wait until DB_JAVA_WALLET is definitely ready"
    ./wait-for-it.sh "$DB_JAVA_WALLET_HOST:$DB_JAVA_WALLET_PORT" -- echo "DB_JAVA_WALLET is up - continuing"
fi

if [[ "$DJANGO_COLLECTSTATIC" = "on" ]]; then
    echo "Collect static files"
    python manage.py collectstatic --no-input
fi

if [[ "$DJANGO_MIGRATE" = "on" ]]; then
    echo "Apply database migrations"
    python manage.py migrate java_wallet --database java_wallet --no-input
    python manage.py migrate --no-input
fi

if [[ "$START_SERVER" = "on" ]]; then
    echo "Starting CMD"
    if [[ "$APP_ENV" = "DEV" ]]; then
        export DJANGO_SERVER_APP="python manage.py runserver 0.0.0.0:5000"
    elif [[ "$APP_ENV" = "PROD" ]]; then
        export DJANGO_SERVER_APP="/usr/local/bin/uwsgi --ini /app/wsgi.ini"
    else
        echo "Unknown APP_ENV: $APP_ENV"
        exit
    fi
    /usr/local/bin/supervisord -c supervisord.conf
fi
