import subprocess
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)
pjsua_process = None

def start_pjsua():
    global pjsua_process
    if pjsua_process is None:
        pjsua_process = subprocess.Popen(
            ["pjsua", "--config-file=/app/pjsua.conf"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

@app.route("/call", methods=["POST"])
def call():
    number = request.json.get("number")
    start_pjsua()
    pjsua_process.stdin.write(f"m sip:{number}\n")
    pjsua_process.stdin.flush()
    return jsonify({"status": "calling", "number": number})

@app.route("/hangup", methods=["POST"])
def hangup():
    if pjsua_process:
        pjsua_process.stdin.write("h\n")
        pjsua_process.stdin.flush()
        return jsonify({"status": "hangup"})
    return jsonify({"error": "not running"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"running": pjsua_process is not None})

if __name__ == "__main__":
    start_pjsua()
    app.run(host="0.0.0.0", port=5000)
