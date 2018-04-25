FROM python:3.6

COPY . /opt/monitor

WORKDIR /opt/monitor

USER root

ENV PATH="/root/.local/bin:$PATH"
ENV INFLUX_HOST=influx
ENV INFLUX_PORT=8086
ENV INFLUX_DB=psstat
ENV INFLUX_USER=dummy
ENV INFLUX_PASSWORD=dummy
ENV ME=$(whoami)

RUN /usr/bin/env python3 -m pip install --user --upgrade pip && /usr/bin/env python3 -m pip install --user -r requirements.txt

