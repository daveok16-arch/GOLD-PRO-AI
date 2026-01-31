import datetime

def market_is_open():
    """
    Forex market:
    Closed Saturday (5) & Sunday (6)
    """
    now = datetime.datetime.utcnow()
    return now.weekday() < 5
