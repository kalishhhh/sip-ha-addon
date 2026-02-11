ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel \
    pjproject \
    pjproject-dev \
    alsa-lib \
    alsa-lib-dev \
    portaudio \
    portaudio-dev \
    gcc \
    g++ \
    make \
    swig \
    linux-headers \
    musl-dev \
    python3-dev

# Install Python packages
RUN pip3 install --no-cache-dir \
    flask \
    requests \
    pjsua2

# Copy data
COPY run.sh /
RUN chmod a+x /run.sh

COPY app.py /app/
COPY pjsua_wrapper.py /app/

WORKDIR /app

CMD [ "/run.sh" ]
