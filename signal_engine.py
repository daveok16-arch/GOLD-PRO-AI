from data_fetcher import fetch_latest_price, fetch_recent_prices
from indicators import ema, rsi

def detect_structure(prices):
    if len(prices) < 20:
        return "RANGE"

    higher_high = prices[-1] > max(prices[-20:-1])
    lower_low = prices[-1] < min(prices[-20:-1])

    if higher_high:
        return "BULL"
    if lower_low:
        return "BEAR"

    return "RANGE"


def generate_signal(symbol):
    price = fetch_latest_price(symbol)
    prices = fetch_recent_prices(symbol, limit=200)

    ema_fast = ema(prices, 50)
    ema_slow = ema(prices, 200)
    rsi_val = rsi(prices)

    structure = detect_structure(prices)

    signal = "HOLD"
    confidence = 50
    trend = "FLAT"

    # ===== SMART MONEY LOGIC =====

    # BULLISH SMC
    if ema_fast > ema_slow and structure == "BULL" and 50 <= rsi_val <= 65:
        signal = "BUY"
        trend = "BULL"
        confidence = 85

    # BEARISH SMC
    elif ema_fast < ema_slow and structure == "BEAR" and 35 <= rsi_val <= 50:
        signal = "SELL"
        trend = "BEAR"
        confidence = 85

    return {
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence,
        "price": round(price, 2),
        "ema_fast": round(ema_fast, 2),
        "ema_slow": round(ema_slow, 2),
        "trend": trend,
        "structure": structure,
        "rsi": round(rsi_val, 2)
    }
