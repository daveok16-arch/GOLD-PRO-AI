import requests
from config import POLYGON_API_KEY, TWELVE_API_KEY

TWELVE_SYMBOL_MAP = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY"
}

def fetch_latest_price(symbol):
    if symbol == "XAUUSD":
        url = f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/prev?apiKey={POLYGON_API_KEY}"
        data = requests.get(url, timeout=10).json()
        return float(data["results"][0]["c"])

    td = TWELVE_SYMBOL_MAP[symbol]
    url = f"https://api.twelvedata.com/price?symbol={td}&apikey={TWELVE_API_KEY}"
    data = requests.get(url, timeout=10).json()
    return float(data["price"])


def fetch_recent_prices(symbol, limit=200):
    closes, highs, lows = [], [], []

    if symbol == "XAUUSD":
        url = f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/range/15/minute/2024-01-01/2026-12-31?apiKey={POLYGON_API_KEY}"
        data = requests.get(url, timeout=10).json()

        for c in data.get("results", [])[-limit:]:
            highs.append(c["h"])
            lows.append(c["l"])
            closes.append(c["c"])

    else:
        td = TWELVE_SYMBOL_MAP[symbol]
        url = f"https://api.twelvedata.com/time_series?symbol={td}&interval=15min&outputsize={limit}&apikey={TWELVE_API_KEY}"
        data = requests.get(url, timeout=10).json()

        for c in reversed(data.get("values", [])):
            highs.append(float(c["high"]))
            lows.append(float(c["low"]))
            closes.append(float(c["close"]))

    return closes, highs, lows

def fetch_recent_prices(symbol, limit=200, timeframe="15m"):
    import requests
    from config import POLYGON_API_KEY, TWELVE_API_KEY

    # ---- GOLD (Polygon) ----
    if symbol == "XAUUSD":
        tf_map = {"15m": "15", "1h": "60"}
        mult = tf_map.get(timeframe, "15")

        url = (
            f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/"
            f"range/{mult}/minute/{limit}?adjusted=true&apiKey={POLYGON_API_KEY}"
        )

        r = requests.get(url, timeout=10)
        data = r.json()

        if "results" not in data:
            raise RuntimeError("Polygon timeframe not supported by your plan")

        closes = [c["c"] for c in data["results"]]
        highs = [c["h"] for c in data["results"]]
        lows = [c["l"] for c in data["results"]]
        return closes, highs, lows

    # ---- FOREX (TwelveData) ----
    from data_fetcher import TWELVE_SYMBOL_MAP
    td_symbol = TWELVE_SYMBOL_MAP[symbol]

    interval = "15min" if timeframe == "15m" else "1h"
    url = (
        f"https://api.twelvedata.com/time_series?"
        f"symbol={td_symbol}&interval={interval}&outputsize={limit}&apikey={TWELVE_API_KEY}"
    )

    r = requests.get(url, timeout=10)
    data = r.json()

    values = data.get("values", [])
    closes = [float(v["close"]) for v in values][::-1]
    highs = [float(v["high"]) for v in values][::-1]
    lows = [float(v["low"]) for v in values][::-1]

    return closes, highs, lows
