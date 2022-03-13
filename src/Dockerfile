FROM python:3.8.5-alpine

EXPOSE 5000

COPY . /src
WORKDIR /src

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python server.py