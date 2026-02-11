#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

# Read configuration
SIP_SERVER=$(bashio::config 'sip_server')
EXTENSION=$(bashio::config 'extension')
PASSWORD=$(bashio::config 'password')
PORT=$(bashio::config 'port')
LOG_LEVEL=$(bashio::config 'log_level')

# Validate configuration
if [ -z "$SIP_SERVER" ]; then
    bashio::log.error "SIP server is not configured!"
    exit 1
fi

if [ -z "$EXTENSION" ]; then
    bashio::log.error "Extension is not configured!"
    exit 1
fi

if [ -z "$PASSWORD" ]; then
    bashio::log.error "Password is not configured!"
    exit 1
fi

bashio::log.info "Starting SIP Softphone..."
bashio::log.info "SIP Server: ${SIP_SERVER}"
bashio::log.info "Extension: ${EXTENSION}"
bashio::log.info "Port: ${PORT}"
bashio::log.info "Log Level: ${LOG_LEVEL}"

# Export configuration as environment variables
export SIP_SERVER
export EXTENSION
export PASSWORD
export PORT
export LOG_LEVEL

# Start the application
exec python3 /app/app.py
