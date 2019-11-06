FROM python:3.7.4

RUN mkdir -p /data/symphony
WORKDIR /data/symphony

COPY ./venv /data/symphony/venv
COPY /usr/local/bin /usr/local/bin
COPY /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY python /data/symphony/

EXPOSE 8080

CMD [ "python3", "./main_rsa.py" ]
