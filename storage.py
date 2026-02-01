import json
import os

SIGNALS_FILE = "signals.json"

def load_signals():
    if not os.path.exists(SIGNALS_FILE):
        return []
    with open(SIGNALS_FILE, "r") as f:
        return json.load(f)

def save_signal(signal):
    signals = load_signals()
    signals.append(signal)
    with open(SIGNALS_FILE, "w") as f:
        json.dump(signals, f, indent=2)
