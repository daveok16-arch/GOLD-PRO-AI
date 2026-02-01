from collections import defaultdict

def best_trading_hour(signals):
    buckets = defaultdict(list)

    for s in signals:
        try:
            hour = int(s["time"][11:13])
            buckets[hour].append(float(s["confidence"]))
        except Exception:
            continue

    best = None
    best_avg = 0

    for h, confs in buckets.items():
        avg = sum(confs) / len(confs)
        if avg > best_avg:
            best_avg = avg
            best = h

    if best is None:
        return {}

    return {
        "hour": best,
        "avg_confidence": round(best_avg, 2),
        "signals": len(buckets[best])
    }
