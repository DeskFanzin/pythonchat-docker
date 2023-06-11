FROM python:3.8.10-alpine

RUN pip install --upgrade pip

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 --threads 100 wsgi:app

EXPOSE 5000

