#!/bin/bash

echo "Apply database migrations"
./manage.py migrate

echo "Start server"
./manage.py runserver 0.0.0.0:8000
