from data_fetcher import fetch_latest_price, fetch_recent_prices
from indicators import ema, rsi


def generate_signal(symbol):
    prices = fetch_recent_prices(symbol, limit=200)
    current_price = fetch_latest_price(symbol)

    ema_fast = ema(prices, 20)
    ema_slow = ema(prices, 50)
    rsi_val = rsi(prices)

    if ema_fast > ema_slow:
        trend = "BULL"
    elif ema_fast < ema_slow:
        trend = "BEAR"
    else:
        trend = "FLAT"

    if trend == "BULL" and rsi_val < 70:
        signal = "BUY"
        confidence = 80
    elif trend == "BEAR" and rsi_val > 30:
        signal = "SELL"
        confidence = 80
    else:
        signal = "HOLD"
        confidence = 50

    return {
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence,
        "price": current_price,
        "ema_fast": ema_fast,
        "ema_slow": ema_slow,
        "trend": trend,
        "rsi": rsi_val
    }
