#!/usr/bin/env sh

set -o errexit
set -o nounset

if [ "$DJANGO_COLLECTSTATIC" = "on" ]; then
	echo "Collect static files"
	python manage.py collectstatic --no-input
fi

if [ "$DJANGO_MIGRATE" = "on" ]; then
	echo "Apply database migrations"
	python manage.py migrate java_wallet --database java_wallet --no-input
	python manage.py migrate --no-input
fi

if [ "$START_SERVER" = "on" ]; then
	echo "Starting server"
	if [ "$APP_ENV" = "development" ]; then
		python manage.py runserver 0.0.0.0:5000
	elif [ "$APP_ENV" = "production" ]; then
		/usr/local/bin/supervisord -c /supervisord.conf
	else
		echo "Unknown APP_ENV: $APP_ENV"
		echo "Application will not start."
		exit 1
	fi
fi
