FROM python:3.8-slim-buster as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
RUN pip3 install -t /install python-telegram-bot

FROM base
COPY --from=builder /install /usr/local/lib/python3.8/site-packages
COPY src /app
WORKDIR /app

CMD [ "python", "-u", "main.py" ]