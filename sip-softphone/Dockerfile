FROM ghcr.io/home-assistant/aarch64-addon-base:latest

RUN apk add --no-cache \
    pjproject \
    python3 \
    py3-pip \
    py3-virtualenv \
    alsa-lib \
    alsa-utils \
    jq

RUN python3 -m venv /venv

COPY requirements.txt /
RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /requirements.txt

COPY server.py /app/server.py

RUN mkdir -p /etc/services.d/sip
COPY run.sh /etc/services.d/sip/run
RUN chmod +x /etc/services.d/sip/run
