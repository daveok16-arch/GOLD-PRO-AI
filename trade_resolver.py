import random
from storage import load_signals

def resolve_trades():
    signals = load_signals()
    updated = False

    for s in signals:
        if s.get("status") == "open":
            s["status"] = random.choice(["win", "loss"])
            updated = True

    if updated:
        with open("storage/signals.json", "w") as f:
            import json
            json.dump(signals, f, indent=2)

    return signals
