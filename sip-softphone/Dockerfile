ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq

RUN mkdir -p /etc/services.d/test

COPY run.sh /etc/services.d/test/run
RUN chmod +x /etc/services.d/test/run
