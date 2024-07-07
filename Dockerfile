# Set the python version as a build-time argument with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION} AS base

# Create a virtual environment and set it as the default
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip and install dependencies for building the project
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev libjpeg-dev libcairo2 gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /code

# Copy requirements file and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project code into the container
COPY . /code

# Set the Django project name as a build argument
ARG PROJ_NAME="cinespectra"

# Create a script to run the Django project
RUN echo '#!/bin/bash\n\
RUN_PORT="${PORT:-8000}"\n\
python manage.py migrate --no-input\n\
gunicorn ${PROJ_NAME}.wsgi:application --bind "0.0.0.0:$RUN_PORT"' > ./paracord_runner.sh && \
    chmod +x ./paracord_runner.sh

# Run the Django project via the script when the container starts
CMD ["./paracord_runner.sh"]
