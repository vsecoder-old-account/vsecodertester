FROM python:3

RUN pip install --upgrade pip && \
    pip install requests

FROM node:12.18.1

RUN npm install
