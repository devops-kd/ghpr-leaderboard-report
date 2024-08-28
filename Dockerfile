FROM python:3.11.6-alpine3.18

USER 1000

ADD ./src /
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "./main.py"]