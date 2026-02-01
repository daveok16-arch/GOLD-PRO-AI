from flask import Flask, jsonify
from signal_engine import generate_signal
from storage import load_signals, save_signal

app = Flask(__name__)

@app.route("/signal/latest")
def latest_signal():
    signals = load_signals()
    return jsonify(signals[-1] if signals else {})

@app.route("/signal/generate")
def generate():
    signal = generate_signal()
    save_signal(signal)
    return jsonify(signal)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
