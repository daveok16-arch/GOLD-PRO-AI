import json
import os
from datetime import datetime

STATE_FILE = "signals.json"

def load_signals():
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_signal(signal):
    signals = load_signals()
    signal["time"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    signals.insert(0, signal)

    with open(STATE_FILE, "w") as f:
        json.dump(signals[:100], f, indent=2)
