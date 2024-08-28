FROM python:3.11.6-alpine3.18

RUN adduser --disabled-password --uid 1000 devuser
USER devuser

ADD ./src /
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "./main.py"]