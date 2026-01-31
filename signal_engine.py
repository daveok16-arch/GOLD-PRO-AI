from indicators import ema, rsi, macd

def simple_trend_check(data):
    try:
        closes = [float(x["close"]) for x in data["values"][:30]][::-1]

        if len(closes) < 30:
            return None

        ema_fast = ema(closes, 9)
        ema_slow = ema(closes, 21)
        rsi_val = rsi(closes)
        macd_val = macd(closes)

        score = 0
        if ema_fast > ema_slow:
            score += 1
        if rsi_val > 50:
            score += 1
        if macd_val > 0:
            score += 1

        return {
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "rsi": rsi_val,
            "macd": macd_val,
            "score": score
        }

    except Exception as e:
        return None


def generate_signal(market_trends):
    confidence = 0

    gold = market_trends.get("XAUUSD")
    btc = market_trends.get("BTC")
    vix = market_trends.get("VIX")

    if gold and gold["score"] >= 2:
        confidence += 40

    if btc and btc["score"] >= 2:
        confidence += 30

    if vix and vix["rsi"] < 50:
        confidence += 20

    if confidence >= 60:
        return "BUY_XAUUSD", confidence

    return "NO_TRADE", confidence
