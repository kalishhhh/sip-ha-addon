FROM ghcr.io/home-assistant/aarch64-base:3.19

RUN apk add --no-cache \
    pjproject \
    python3 \
    py3-pip \
    py3-virtualenv \
    alsa-lib \
    alsa-utils \
    jq

# Create virtual environment
RUN python3 -m venv /venv

COPY requirements.txt /
RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /requirements.txt

COPY server.py /app/server.py
# s6 service setup
RUN mkdir -p /etc/services.d/sip

COPY run.sh /etc/services.d/sip/run
RUN chmod +x /etc/services.d/sip/run
