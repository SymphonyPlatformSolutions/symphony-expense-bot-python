FROM python:3.7.4

RUN mkdir -p /data/symphony
WORKDIR /data/symphony

COPY python /data/symphony/
COPY requirements.txt /data/symphony

EXPOSE 8080


RUN pip install -r requirements.txt
CMD [ "python3", "./main_rsa.py" ]
