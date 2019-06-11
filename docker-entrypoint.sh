#!/usr/bin/env bash

set -e

if [ ! -z $DB_DEFAULT_HOST ]; then
    echo "Wait until DB_DEFAULT is definitely ready"
    ./wait-for-it.sh $DB_DEFAULT_HOST:$DB_DEFAULT_PORT -- echo "DB_DEFAULT is up - continuing"
fi

if [ ! -z $DB_JAVA_WALLET_HOST ]; then
    echo "Wait until DB_JAVA_WALLET is definitely ready"
    ./wait-for-it.sh $DB_JAVA_WALLET_HOST:$DB_JAVA_WALLET_PORT -- echo "DB_JAVA_WALLET is up - continuing"
fi

if [ "$DJANGO_COLLECTSTATIC" = "on" ]; then
    echo "Collect static files"
    python manage.py collectstatic --noinput
fi

if [ "$DJANGO_MIGRATE" = "on" ]; then
    echo "Apply database migrations"
    python manage.py migrate java_wallet --database java_wallet
    python manage.py migrate
fi

if [ "$START_CMD" = "on" ]; then
    echo "Starting CMD"
    exec "$@"
fi
