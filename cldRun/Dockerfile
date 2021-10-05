# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.9

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN mkdir -p /app/input
RUN mkdir -p /app/output

RUN chmod +x /app/main.py

#PORT env variable assigned by gcloud
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app