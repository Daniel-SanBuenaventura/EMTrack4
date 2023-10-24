# syntax=docker/dockerfile:1
FROM python:3.9.7-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt update && apt install -y sudo apt-transport-https \
  && apt install -y --allow-unauthenticated --no-install-recommends \
    build-essential \
    apt-utils \
    nano \
    dumb-init && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /sample_receiver/
WORKDIR /sample_receiver
RUN pip install -r requirements.txt
WORKDIR /er
COPY pytest.ini manage.py ./run.sh /er/
COPY external_receiver /er/external_receiver/
RUN sudo chmod -R 777 /er/
CMD ["/er/run.sh"]
COPY . /sample_receiver/
