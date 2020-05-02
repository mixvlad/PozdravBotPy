FROM python:3.8-slim-buster

RUN pip3 install --no-cache python-telegram-bot

COPY /src /app
WORKDIR /app

CMD [ "python", "main.py" ]