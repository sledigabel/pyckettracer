FROM alpine:latest
MAINTAINER sledigabel@gmail.com

RUN apk update
RUN apk add gcc python python-dev py-pip libpcap libpcap-dev libdnet g++

COPY GeoLite2-City.mmdb.gz /tmp
RUN gzip -d /tmp/GeoLite2-City.mmdb.gz

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY pyckettracer.py /tmp
RUN chmod 755 /tmp/pyckettracer.py

CMD /bin/sh
