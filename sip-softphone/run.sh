#!/usr/bin/with-contenv bash

CONFIG_PATH=/data/options.json

echo "Loading SIP configuration..."

SIP_SERVER=$(jq -r '.sip_server' $CONFIG_PATH)
EXTENSION=$(jq -r '.extension' $CONFIG_PATH)
PASSWORD=$(jq -r '.password' $CONFIG_PATH)

mkdir -p /app

cat > /app/pjsua.conf <<EOF
--id sip:$EXTENSION@$SIP_SERVER
--registrar sip:$SIP_SERVER
--realm *
--username $EXTENSION
--password $PASSWORD
--auto-answer 200
--null-audio
EOF

echo "Starting SIP Softphone..."

exec /venv/bin/python /app/server.py
