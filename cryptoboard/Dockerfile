# syntax=docker/dockerfile:1
# FROM python:alpine3.13
FROM python:3.10-slim-buster

# set work directory
WORKDIR /usr/src/cryptoboard

# set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

RUN apt-get update
RUN apt-get install -y build-essential libpq-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/cryptoboard/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/cryptoboard/
EXPOSE 8000
CMD ["flask", "--debug", "run"]