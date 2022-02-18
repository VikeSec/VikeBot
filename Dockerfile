FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x bot.py

ENV PYTHONUNBUFFERED 1
CMD [ "python3.10", "bot.py" ]
