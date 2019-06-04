#!/bin/bash

echo "Apply database migrations"
./manage.py migrate java_wallet --database java_wallet
./manage.py migrate

echo "Start server"
./manage.py runserver 0.0.0.0:8000
