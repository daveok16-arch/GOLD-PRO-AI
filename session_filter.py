from datetime import datetime, timezone

def is_trading_session():
    now = datetime.now(timezone.utc)
    hour = now.hour

    # London: 07–16 UTC
    if 7 <= hour < 16:
        return "LONDON"

    # New York: 12–21 UTC
    if 12 <= hour < 21:
        return "NEW YORK"

    return None
