#!/usr/bin/env python3
"""
SIP Softphone for Home Assistant
Handles incoming and outgoing SIP calls
"""

import os
import sys
import json
import logging
import signal
from flask import Flask, request, jsonify
from pjsua_wrapper import SIPSoftphone

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Read configuration
SIP_SERVER = os.getenv('SIP_SERVER')
EXTENSION = os.getenv('EXTENSION')
PASSWORD = os.getenv('PASSWORD')
PORT = int(os.getenv('PORT', 5060))

# Initialize Flask app
app = Flask(__name__)

# Initialize SIP softphone
softphone = None

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("Shutting down...")
    if softphone:
        softphone.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    if softphone and softphone.running:
        return jsonify({"status": "healthy", "sip_registered": True}), 200
    else:
        return jsonify({"status": "unhealthy", "sip_registered": False}), 503


@app.route('/call', methods=['POST'])
def make_call():
    """Make an outgoing call"""
    try:
        data = request.get_json()
        destination = data.get('destination')
        
        if not destination:
            return jsonify({"error": "destination is required"}), 400
        
        if not softphone or not softphone.running:
            return jsonify({"error": "SIP softphone not running"}), 503
        
        call = softphone.make_call(destination)
        
        if call:
            return jsonify({
                "status": "success",
                "message": f"Call initiated to {destination}"
            }), 200
        else:
            return jsonify({"error": "Failed to initiate call"}), 500
            
    except Exception as e:
        logger.error(f"Error making call: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/hangup', methods=['POST'])
def hangup():
    """Hang up active calls"""
    try:
        if not softphone or not softphone.running:
            return jsonify({"error": "SIP softphone not running"}), 503
        
        softphone.hangup_all()
        return jsonify({"status": "success", "message": "Call hung up"}), 200
        
    except Exception as e:
        logger.error(f"Error hanging up: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """Get softphone status"""
    try:
        if softphone and softphone.running:
            return jsonify({
                "registered": True,
                "server": SIP_SERVER,
                "extension": EXTENSION
            }), 200
        else:
            return jsonify({"registered": False}), 200
            
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({"error": str(e)}), 500


def main():
    """Main function"""
    global softphone
    
    logger.info("Starting SIP Softphone...")
    logger.info(f"Server: {SIP_SERVER}")
    logger.info(f"Extension: {EXTENSION}")
    logger.info(f"Port: {PORT}")
    
    # Initialize and start SIP softphone
    softphone = SIPSoftphone(SIP_SERVER, EXTENSION, PASSWORD, PORT)
    
    if not softphone.start():
        logger.error("Failed to start SIP softphone")
        sys.exit(1)
    
    logger.info("SIP Softphone started successfully")
    
    # Start Flask web server for API
    logger.info("Starting API server on port 8099...")
    app.run(host='0.0.0.0', port=8099, debug=False)


if __name__ == '__main__':
    main()
