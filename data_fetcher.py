import requests
import time
from config import POLYGON_API_KEY, TWELVE_API_KEY

TWELVE_SYMBOL_MAP = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def safe_json(response):
    try:
        return response.json()
    except Exception:
        raise RuntimeError(f"Invalid API response: {response.text[:200]}")


def fetch_latest_price(symbol):
    # ===== GOLD (Polygon) =====
    if symbol == "XAUUSD":
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/prev"
            f"?adjusted=true&apiKey={POLYGON_API_KEY}"
        )
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = safe_json(r)

        if "results" not in data:
            raise RuntimeError(f"Polygon error: {data}")

        return float(data["results"][0]["c"])

    # ===== FOREX (TwelveData) =====
    td_symbol = TWELVE_SYMBOL_MAP.get(symbol)
    if not td_symbol:
        raise RuntimeError(f"Unsupported symbol: {symbol}")

    url = (
        f"https://api.twelvedata.com/price"
        f"?symbol={td_symbol}&apikey={TWELVE_API_KEY}"
    )

    r = requests.get(url, headers=HEADERS, timeout=10)
    data = safe_json(r)

    if "price" not in data:
        raise RuntimeError(f"TwelveData error: {data}")

    return float(data["price"])


def fetch_recent_prices(symbol, limit=200):
    prices = []

    # ===== GOLD (Polygon) — SAFE FALLBACK =====
    if symbol == "XAUUSD":
        # Polygon free plan limitation → use synthetic HTF
        price = fetch_latest_price(symbol)
        return [price] * limit

    # ===== FOREX (TwelveData) =====
    td_symbol = TWELVE_SYMBOL_MAP.get(symbol)
    if not td_symbol:
        raise RuntimeError(f"Unsupported symbol: {symbol}")

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={td_symbol}"
        f"&interval=5min"
        f"&outputsize={limit}"
        f"&apikey={TWELVE_API_KEY}"
    )

    r = requests.get(url, headers=HEADERS, timeout=10)
    data = safe_json(r)

    if "values" not in data:
        raise RuntimeError(f"TwelveData candle error: {data}")

    for candle in reversed(data["values"]):
        prices.append(float(candle["close"]))

    return prices
