FROM python:3.7

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

RUN mkdir /app

WORKDIR /app

COPY ./books /app
COPY ./deploy/* /app/

ENV PYTHONPATH=/app

EXPOSE 80

CMD ["/app/start.sh"]
