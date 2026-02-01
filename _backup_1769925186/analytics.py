from collections import defaultdict
from state import load_signals

def build_analytics():
    signals = load_signals()

    summary = {
        "total_signals": len(signals),
        "latest_signal_time": None,
        "buy_sell_ratio": {"BUY": 0, "SELL": 0},
        "confidence_distribution": {
            "60-69": 0,
            "70-79": 0,
            "80-100": 0
        },
        "by_symbol": defaultdict(lambda: {
            "count": 0,
            "confidence_sum": 0,
            "avg_confidence": 0
        })
    }

    for s in signals:
        summary["latest_signal_time"] = s["time"]
        summary["buy_sell_ratio"][s["signal"]] += 1

        c = s["confidence"]
        if c < 70:
            summary["confidence_distribution"]["60-69"] += 1
        elif c < 80:
            summary["confidence_distribution"]["70-79"] += 1
        else:
            summary["confidence_distribution"]["80-100"] += 1

        sym = summary["by_symbol"][s["symbol"]]
        sym["count"] += 1
        sym["confidence_sum"] += c

    for sym in summary["by_symbol"].values():
        sym["avg_confidence"] = round(
            sym["confidence_sum"] / sym["count"], 2
        )

    return summary


def best_performing_symbols():
    signals = load_signals()
    stats = defaultdict(lambda: {"count": 0, "confidence_sum": 0})

    for s in signals:
        sym = stats[s["symbol"]]
        sym["count"] += 1
        sym["confidence_sum"] += s["confidence"]

    ranking = []
    for symbol, data in stats.items():
        avg_conf = data["confidence_sum"] / data["count"]
        score = round(avg_conf * data["count"], 2)

        ranking.append({
            "symbol": symbol,
            "signals": data["count"],
            "avg_confidence": round(avg_conf, 2),
            "score": score
        })

    ranking.sort(key=lambda x: x["score"], reverse=True)
    return ranking


def recent_signals(limit=20):
    signals = []
    try:
        with open("signals.log", "r") as f:
            lines = f.readlines()[-limit:]

        for line in reversed(lines):
            parts = line.strip().split(",")

            signals.append({
                "time": parts[0] if len(parts) > 0 else "",
                "symbol": parts[1] if len(parts) > 1 else "",
                "timeframe": parts[2] if len(parts) > 2 else "-",
                "side": parts[3] if len(parts) > 3 else "",
                "confidence": float(parts[4]) if len(parts) > 4 else 0
            })
    except Exception as e:
        print("Signal history error:", e)

    return signals

from collections import defaultdict
from datetime import datetime

def time_of_day_analytics(signals):
    hours = defaultdict(lambda: {"count": 0, "confidence_sum": 0})

    for s in signals:
        try:
            hour = datetime.fromisoformat(s["time"]).hour
        except Exception:
            continue

        hours[hour]["count"] += 1
        hours[hour]["confidence_sum"] += s["confidence"]

    result = []
    for hour, data in sorted(hours.items()):
        avg_conf = round(data["confidence_sum"] / data["count"], 2)
        result.append({
            "hour": hour,
            "signals": data["count"],
            "avg_confidence": avg_conf
        })

    return result

def best_trading_hour(signals):
    """
    Returns the single best hour based on:
    - highest average confidence
    - minimum 1 signal
    """
    hourly = {}

    for s in signals:
        hour = int(s["time"].split(" ")[1].split(":")[0])
        hourly.setdefault(hour, {"confidence": 0, "count": 0})
        hourly[hour]["confidence"] += s["confidence"]
        hourly[hour]["count"] += 1

    if not hourly:
        return {}

    best_hour = max(
        hourly.items(),
        key=lambda x: x[1]["confidence"] / x[1]["count"]
    )

    hour, data = best_hour
    return {
        "hour": hour,
        "avg_confidence": round(data["confidence"] / data["count"], 2),
        "signals": data["count"]
    }

def performance_metrics(signals):
    """
    Calculates win rate and expectancy.
    Assumes each signal has:
    - signal: BUY / SELL
    - outcome: WIN / LOSS (if missing, ignored)
    - confidence
    """
    wins = 0
    losses = 0
    total = 0
    confidence_sum = 0

    for s in signals:
        outcome = s.get("outcome")
        if outcome not in ("WIN", "LOSS"):
            continue

        total += 1
        confidence_sum += s.get("confidence", 0)

        if outcome == "WIN":
            wins += 1
        else:
            losses += 1

    if total == 0:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "expectancy": 0
        }

    win_rate = round((wins / total) * 100, 2)
    avg_conf = confidence_sum / total
    expectancy = round((wins / total) - (losses / total), 3)

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "avg_confidence": round(avg_conf, 2),
        "expectancy": expectancy
    }

def expectancy_leaderboard(signals):
    stats = {}

    for s in signals:
        sym = s["symbol"]
        pnl = s.get("pnl", 0)

        if sym not in stats:
            stats[sym] = {
                "wins": 0,
                "losses": 0,
                "win_sum": 0,
                "loss_sum": 0,
                "trades": 0
            }

        stats[sym]["trades"] += 1

        if pnl > 0:
            stats[sym]["wins"] += 1
            stats[sym]["win_sum"] += pnl
        elif pnl < 0:
            stats[sym]["losses"] += 1
            stats[sym]["loss_sum"] += abs(pnl)

    leaderboard = []

    for sym, v in stats.items():
        if v["trades"] == 0:
            continue

        win_rate = v["wins"] / v["trades"] if v["wins"] else 0
        loss_rate = v["losses"] / v["trades"] if v["losses"] else 0
        avg_win = v["win_sum"] / v["wins"] if v["wins"] else 0
        avg_loss = v["loss_sum"] / v["losses"] if v["losses"] else 0

        expectancy = (win_rate * avg_win) - (loss_rate * avg_loss)

        leaderboard.append({
            "symbol": sym,
            "expectancy": round(expectancy, 4),
            "win_rate": round(win_rate * 100, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "trades": v["trades"]
        })

    leaderboard.sort(key=lambda x: x["expectancy"], reverse=True)
    return leaderboard

def expectancy(signals):
    """
    Expectancy = (Win% * Avg Win) - (Loss% * Avg Loss)
    """
    if not signals:
        return {
            "expectancy": 0,
            "wins": 0,
            "losses": 0
        }

    wins = []
    losses = []

    for s in signals:
        pnl = s.get("pnl")
        if pnl is None:
            continue
        if pnl > 0:
            wins.append(pnl)
        elif pnl < 0:
            losses.append(abs(pnl))

    total = len(wins) + len(losses)
    if total == 0:
        return {
            "expectancy": 0,
            "wins": 0,
            "losses": 0
        }

    win_rate = len(wins) / total
    loss_rate = len(losses) / total

    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    expectancy_value = (win_rate * avg_win) - (loss_rate * avg_loss)

    return {
        "expectancy": round(expectancy_value, 2),
        "win_rate": round(win_rate * 100, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "wins": len(wins),
        "losses": len(losses)
    }
