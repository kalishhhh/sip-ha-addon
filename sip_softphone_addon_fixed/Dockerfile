ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    pjproject \
    alsa-lib \
    alsa-utils \
    bash \
    jq

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages \
    flask==3.0.0 \
    requests==2.31.0

# Copy application files
COPY run.sh /
RUN chmod a+x /run.sh

COPY app_simple.py /app/app.py

WORKDIR /app

CMD [ "/run.sh" ]
