import json
from datetime import datetime

FILE = "trade_history.json"

def load_trades():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_trade(trade):
    data = load_trades()
    data.append(trade)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def record_trade(symbol, signal, entry, sl, tp, result, rr):
    trade = {
        "time": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "signal": signal,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "result": result,  # WIN / LOSS
        "rr": rr
    }
    save_trade(trade)
