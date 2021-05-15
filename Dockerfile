# Dockerfile
# Pull base image

FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

#install getttext to work with localization
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

# Copy project
COPY . /code/