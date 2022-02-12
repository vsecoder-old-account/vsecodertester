FROM python:3

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN useradd user

USER user

WORKDIR /vsecoder