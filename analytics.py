import json
import os

STATS_FILE = "trade_history.json"

def save_trade(trade):
    history = load_history()
    history.append(trade)

    with open(STATS_FILE, "w") as f:
        json.dump(history, f, indent=2, default=str)

def load_history():
    if not os.path.exists(STATS_FILE):
        return []
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def calculate_stats(starting_balance):
    history = load_history()
    if not history:
        return {}

    balance = starting_balance
    peak = balance
    max_dd = 0
    wins = 0

    for t in history:
        pnl = t.get("pnl", 0)
        balance += pnl
        peak = max(peak, balance)
        dd = peak - balance
        max_dd = max(max_dd, dd)

        if pnl > 0:
            wins += 1

    total = len(history)
    return {
        "total_trades": total,
        "wins": wins,
        "losses": total - wins,
        "win_rate": round((wins / total) * 100, 2),
        "total_pnl": round(balance - starting_balance, 2),
        "max_drawdown": round(max_dd, 2),
        "final_balance": round(balance, 2)
    }
