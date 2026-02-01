from collections import Counter

def performance_from_signals(signals):
    wins = 0
    losses = 0

    for s in signals:
        result = s.get("result")
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1

    total = wins + losses
    expectancy = round((wins - losses) / total, 2) if total > 0 else 0

    return {
        "wins": wins,
        "losses": losses,
        "expectancy": expectancy
    }


def best_trading_hour(signals):
    hour_stats = {}

    for s in signals:
        hour = s.get("hour")
        result = s.get("result")

        if hour is None:
            continue

        if hour not in hour_stats:
            hour_stats[hour] = {"wins": 0, "losses": 0}

        if result == "win":
            hour_stats[hour]["wins"] += 1
        elif result == "loss":
            hour_stats[hour]["losses"] += 1

    best_hour = None
    best_score = -999

    for hour, stats in hour_stats.items():
        score = stats["wins"] - stats["losses"]
        if score > best_score:
            best_score = score
            best_hour = hour

    return best_hour
