FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh
RUN pip3 install -r requirements.txt

COPY ./flask/store_locator .

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]