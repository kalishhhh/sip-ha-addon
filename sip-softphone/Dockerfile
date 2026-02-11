ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    pjsip \
    python3 \
    py3-pip \
    alsa-lib \
    alsa-utils \
    jq

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY server.py /app/server.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

WORKDIR /app
CMD ["/run.sh"]
