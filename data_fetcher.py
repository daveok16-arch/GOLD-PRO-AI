import time
import requests
from config import POLYGON_API_KEY, TWELVE_API_KEY

TWELVE_SYMBOL_MAP = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY"
}

# ===============================
# Latest price (SAFE)
# ===============================
def fetch_latest_price(symbol):

    if symbol == "XAUUSD":
        url = (
            "https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/"
            f"prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        )
        r = requests.get(url, timeout=10)
        data = r.json()

        if "results" not in data:
            raise RuntimeError("Polygon blocked XAUUSD price access")

        return float(data["results"][0]["c"])

    td_symbol = TWELVE_SYMBOL_MAP.get(symbol)
    if not td_symbol:
        raise RuntimeError(f"Unsupported symbol: {symbol}")

    url = (
        "https://api.twelvedata.com/price?"
        f"symbol={td_symbol}&apikey={TWELVE_API_KEY}"
    )
    r = requests.get(url, timeout=10)
    data = r.json()

    if "price" not in data:
        raise RuntimeError(f"TwelveData price error: {data}")

    return float(data["price"])


# ===============================
# Recent prices (FAIL-SAFE)
# ===============================
def fetch_recent_prices(symbol, limit=200):

    # ===== XAUUSD =====
    if symbol == "XAUUSD":
        try:
            now_ms = int(time.time() * 1000)
            from_ms = now_ms - (limit * 5 * 60 * 1000)

            url = (
                f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/"
                f"range/5/minute/{from_ms}/{now_ms}"
                f"?adjusted=true&sort=asc&limit={limit}&apiKey={POLYGON_API_KEY}"
            )

            r = requests.get(url, timeout=10)
            data = r.json()

            if data.get("status") == "OK" and "results" in data:
                return [float(c["c"]) for c in data["results"]]

        except Exception:
            pass  # silently fall through

        # 🔁 FALLBACK: synthetic candles from latest price
        price = fetch_latest_price("XAUUSD")
        return [price] * limit

    # ===== FOREX =====
    td_symbol = TWELVE_SYMBOL_MAP.get(symbol)
    if not td_symbol:
        raise RuntimeError(f"Unsupported symbol: {symbol}")

    url = (
        "https://api.twelvedata.com/time_series?"
        f"symbol={td_symbol}&interval=1min&outputsize={limit}"
        f"&apikey={TWELVE_API_KEY}"
    )

    r = requests.get(url, timeout=10)
    data = r.json()

    if "values" not in data:
        raise RuntimeError(f"TwelveData candle error: {data}")

    return [float(v["close"]) for v in reversed(data["values"])]
