import json
import os
from datetime import datetime

SIGNALS_FILE = "signals.json"

def log_signal(symbol, timeframe, side, confidence):
    signal = {
        "time": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "tf": timeframe,
        "side": side,
        "confidence": float(confidence)
    }

    data = []
    if os.path.exists(SIGNALS_FILE):
        try:
            with open(SIGNALS_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = []

    data.append(signal)

    with open(SIGNALS_FILE, "w") as f:
        json.dump(data, f, indent=2)
