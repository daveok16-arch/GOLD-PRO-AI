from flask import Flask, jsonify
from storage import load_signals
from collections import Counter

app = Flask(__name__)

def performance_from_signals(signals):
    wins = 0
    losses = 0

    for s in signals:
        if s.get("result") == "win":
            wins += 1
        elif s.get("result") == "loss":
            losses += 1

    total = wins + losses
    expectancy = round((wins - losses) / total, 2) if total else 0

    return {
        "wins": wins,
        "losses": losses,
        "expectancy": expectancy
    }

def best_trading_hour(signals):
    stats = {}

    for s in signals:
        hour = s.get("hour")
        result = s.get("result")
        if hour is None:
            continue

        stats.setdefault(hour, {"win": 0, "loss": 0})
        if result == "win":
            stats[hour]["win"] += 1
        elif result == "loss":
            stats[hour]["loss"] += 1

    best = None
    score = -999
    for h, v in stats.items():
        s = v["win"] - v["loss"]
        if s > score:
            score = s
            best = h

    return best

@app.route("/analytics/performance")
def performance():
    signals = load_signals()
    return jsonify(performance_from_signals(signals))

@app.route("/analytics/best-hour")
def best_hour():
    signals = load_signals()
    return jsonify({"best_hour": best_trading_hour(signals)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
