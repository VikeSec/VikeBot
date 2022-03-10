FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt update && \
    apt upgrade -y && \
    apt install gcc &&
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1
CMD [ "python3.10", "bot.py" ]
