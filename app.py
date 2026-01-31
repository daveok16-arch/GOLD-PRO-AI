from flask import Flask, jsonify
from main import run_cycle

app = Flask(__name__)

latest_signals = []

@app.route("/")
def home():
    return {
        "status": "GOLD-PRO-AI RUNNING",
        "signals": latest_signals
    }

@app.route("/run")
def run_bot():
    signal = run_cycle(web_mode=True)
    if signal:
        latest_signals.append(signal)
    return jsonify({"ok": True, "signal": signal})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
