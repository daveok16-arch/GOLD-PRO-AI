from flask import Flask, jsonify
from main import run_scan
from state import load_signals
from utils import market_is_open
from analytics import build_analytics
import threading
import time

app = Flask(__name__)

SCAN_INTERVAL = 300  # 5 minutes

def auto_scan_loop():
    while True:
        if market_is_open():
            print("[AUTO] Market open → scanning")
            run_scan()
        else:
            print("[AUTO] Market closed → sleeping")

        time.sleep(SCAN_INTERVAL)

@app.route("/")
def home():
    return jsonify({
        "market_open": market_is_open(),
        "banner": None if market_is_open() else "Market is closed or low liquidity (weekend)",
        "signals": load_signals()
    })

@app.route("/analytics")
def analytics():
    return jsonify(build_analytics())

@app.route("/status")
def status():
    return jsonify({
        "market_open": market_is_open()
    })

if __name__ == "__main__":
    threading.Thread(target=auto_scan_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)
