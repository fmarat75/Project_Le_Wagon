FROM python:3.10.6-buster

COPY model /model
COPY requirements.txt /requirements.txt
COPY .env /.dockerenv

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn model.api:app --host 0.0.0.0
