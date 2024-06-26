FROM python:3.11-alpine

LABEL "title" = "kislozelje api tests"

WORKDIR ./usr/tests

VOLUME /alluredir

RUN apk update && apk add --no-cache bash

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD pytest --alluredir=alluredir