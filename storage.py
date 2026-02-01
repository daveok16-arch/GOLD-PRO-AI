import json
import os
from datetime import datetime

STORAGE_FILE = "storage/signals.json"

def load_signals():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_signal(signal: dict):
    signals = load_signals()
    signal["stored_at"] = datetime.utcnow().isoformat()
    signals.append(signal)
    with open(STORAGE_FILE, "w") as f:
        json.dump(signals, f, indent=2)

def get_all_signals():
    return load_signals()
