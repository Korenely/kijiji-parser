FROM python:3.10.4-slim-buster
LABEL maintainer="danulo.kuybida@gmail.com"

ENV PYTHONUNBUFFERED 1

workdir app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .