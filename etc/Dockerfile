FROM python:3.11

RUN mkdir app
WORKDIR app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./etc /etc/
COPY ./src .

ENTRYPOINT ["/usr/bin/sh", "/etc/entrypoint.sh"]
