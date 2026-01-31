import datetime

STATE = {}

def update_signal(symbol, signal, confidence, price):
    STATE[symbol] = {
        "signal": signal,
        "confidence": confidence,
        "price": price,
        "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

def get_state():
    return STATE
