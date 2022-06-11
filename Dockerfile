FROM python:3.9-alpine

ENV PYTHONBUFFERED 1

RUN apk add postgresql-dev gcc bash python3-dev musl-dev

RUN pip install --upgrade pip && pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt && pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN adduser -D user
USER user
