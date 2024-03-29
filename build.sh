#!/bin/bash

# Build the project
echo "Building the project..."
pip install -r requirements.txt

echo "Make Migration..."
py manage.py makemigrations --noinput
py manage.py migrate --noinput

echo "Collect Static..."
py manage.py collectstatic --noinput --clear