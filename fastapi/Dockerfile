FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./sql_app /app/app
