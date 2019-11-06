FROM python:3.7.4

RUN mkdir -p /data/symphony
WORKDIR /data/symphony

COPY ./venv
COPY python/* /data/symphony

EXPOSE 80

CMD [ "python3", "./main_rsa.py" ]
