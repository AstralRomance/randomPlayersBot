FROM python:3.8
RUN apt-get update
RUN mkdir app
WORKDIR /app

ENV RANDOM_DECKS_KEY=""
RUN python -m pip install --upgrade pip
RUN python -m pip install wheel
RUN python -m pip install aiogram
ADD . / /app/
RUN python bot.py
