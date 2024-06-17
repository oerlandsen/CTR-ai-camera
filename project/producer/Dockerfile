FROM python:3.11

WORKDIR /opt/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install fastapi uvicorn requests python-dotenv celery numpy redis

COPY . /opt/