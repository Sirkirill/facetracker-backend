FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY Pipfile Pipfile.lock /api/

RUN pip install pipenv && pipenv install --system

COPY . /api/