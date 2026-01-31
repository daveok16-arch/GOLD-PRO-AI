import random

def generate_signal(symbol, price):
    """
    Dummy logic placeholder (safe & stable).
    Replace later with indicators.
    """

    direction = random.choice(["BUY", "SELL"])
    confidence = random.randint(60, 90)

    return {
        "symbol": symbol,
        "signal": direction,
        "confidence": confidence,
        "price": round(price, 2)
    }
