from datetime import datetime
import pytz

def market_is_open():
    """
    Simple FX market hours check (Mon–Fri, UTC)
    """
    now = datetime.now(pytz.UTC)
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday

    # FX closed Saturday (5) & Sunday (6)
    if weekday >= 5:
        return False

    return True
