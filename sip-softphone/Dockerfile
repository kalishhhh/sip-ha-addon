FROM debian:12

RUN apt update && apt install -y \
    pjsua \
    python3 \
    python3-pip \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY server.py /app/server.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

WORKDIR /app

CMD ["/run.sh"]
