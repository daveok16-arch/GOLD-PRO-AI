import json
import os

STATE_FILE = "signals.json"

def load_signals():
    if not os.path.exists(STATE_FILE):
        return []

    with open(STATE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_signal(entry):
    signals = load_signals()
    signals.append(entry)

    with open(STATE_FILE, "w") as f:
        json.dump(signals, f, indent=2)
