from flask import Flask, jsonify
from main import run_scan
from state import get_signals

app = Flask(__name__)

@app.route("/")
def dashboard():
    return jsonify({
        "status": "GOLD-PRO-AI RUNNING",
        "signals": get_signals()
    })

@app.route("/scan")
def scan():
    results = run_scan()
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
