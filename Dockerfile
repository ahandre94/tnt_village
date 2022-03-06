FROM python:3.10.1

RUN mkdir /app
ADD . /app
COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

CMD python3 /app/bot.py
