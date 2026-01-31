from state import load_signals
from collections import defaultdict

def build_analytics():
    signals = load_signals()

    analytics = {
        "total_signals": len(signals),
        "by_symbol": {},
        "buy_sell_ratio": {"BUY": 0, "SELL": 0},
        "latest_signal_time": None
    }

    confidence_sum = defaultdict(int)
    confidence_count = defaultdict(int)
    symbol_count = defaultdict(int)

    for s in signals:
        symbol = s["symbol"]
        signal = s["signal"]
        confidence = s["confidence"]

        symbol_count[symbol] += 1
        confidence_sum[symbol] += confidence
        confidence_count[symbol] += 1

        analytics["buy_sell_ratio"][signal] += 1
        analytics["latest_signal_time"] = s["time"]

    for symbol in symbol_count:
        analytics["by_symbol"][symbol] = {
            "count": symbol_count[symbol],
            "avg_confidence": round(
                confidence_sum[symbol] / confidence_count[symbol], 2
            )
        }

    return analytics
