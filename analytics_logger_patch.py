from logger import log_signal

def auto_log(signals):
    for s in signals:
        log_signal(
            symbol=s["symbol"],
            timeframe=s.get("tf", "NA"),
            side=s["side"],
            confidence=s["confidence"]
        )
