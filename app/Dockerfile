FROM python:3.8.10-alpine

RUN pip install --upgrade pip

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt

CMD ["python", "wsgi.py"]

EXPOSE 5000
