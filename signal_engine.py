from data_fetcher import fetch_latest_price, fetch_recent_prices
from indicators import ema, rsi, atr
from session_filter import is_trading_session

def trend_direction(closes):
    ema50 = ema(closes[-50:], 50)
    ema200 = ema(closes[-200:], 200)
    if ema50 > ema200:
        return "BULL"
    if ema50 < ema200:
        return "BEAR"
    return "FLAT"

def liquidity_sweep(highs, lows):
    recent_high = max(highs[-20:-5])
    recent_low = min(lows[-20:-5])
    return highs[-1] > recent_high, lows[-1] < recent_low

def break_of_structure(closes, direction):
    if direction == "BULL":
        return closes[-1] > max(closes[-20:-5])
    if direction == "BEAR":
        return closes[-1] < min(closes[-20:-5])
    return False

def generate_signal(symbol):
    if not is_trading_session():
        return {"symbol": symbol, "signal": "HOLD", "reason": "Outside session"}

    price = fetch_latest_price(symbol)

    c15, h15, l15 = fetch_recent_prices(symbol, 200, "15m")
    c1h, _, _ = fetch_recent_prices(symbol, 200, "1h")

    t15 = trend_direction(c15)
    t1h = trend_direction(c1h)

    if t15 != t1h or t15 == "FLAT":
        return {"symbol": symbol, "signal": "HOLD", "reason": "MTF mismatch"}

    sweep_high, sweep_low = liquidity_sweep(h15, l15)

    if t15 == "BULL" and not sweep_low:
        return {"symbol": symbol, "signal": "HOLD", "reason": "No sell-side liquidity sweep"}

    if t15 == "BEAR" and not sweep_high:
        return {"symbol": symbol, "signal": "HOLD", "reason": "No buy-side liquidity sweep"}

    if not break_of_structure(c15, t15):
        return {"symbol": symbol, "signal": "HOLD", "reason": "No BOS"}

    atr_val = atr(h15, l15, c15)
    rsi_val = rsi(c15)

    signal = "BUY" if t15 == "BULL" else "SELL"
    sl = price - (1.5 * atr_val) if signal == "BUY" else price + (1.5 * atr_val)
    tp = price + (3 * atr_val) if signal == "BUY" else price - (3 * atr_val)

    return {
        "symbol": symbol,
        "signal": signal,
        "confidence": 95,
        "price": round(price, 2),
        "trend": t15,
        "rsi": round(rsi_val, 2),
        "SL": round(sl, 2),
        "TP": round(tp, 2),
        "model": "SMC-MTF-BOS"
    }
