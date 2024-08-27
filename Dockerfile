FROM python:3.11.6-alpine3.18

ADD ./src /
RUN pip3 install -r requirements.txt

USER 1000

ENTRYPOINT ["python3", "./main.py"]