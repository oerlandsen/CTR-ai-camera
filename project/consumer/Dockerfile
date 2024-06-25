FROM python:3.11

WORKDIR /opt/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /opt/requirements.txt 
RUN chmod +x /opt/requirements.txt
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx
RUN pip install -r requirements.txt

COPY . /opt/