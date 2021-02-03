FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

RUN mkdir /app

COPY config/dev-service-account.json /app
COPY config/prod-service-account.json /app
COPY src /app

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 index:app
