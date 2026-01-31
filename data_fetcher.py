import requests
from config import POLYGON_API_KEY, TWELVE_API_KEY

# Map internal symbols → TwelveData symbols
TWELVE_SYMBOL_MAP = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY"
}

def fetch_market_data(symbol, timeframe=None):
    """
    Returns:
    {
        "symbol": str,
        "price": float
    }
    """

    # ===== GOLD (Polygon) =====
    if symbol == "XAUUSD":
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/"
            f"prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        )
        r = requests.get(url, timeout=10)
        data = r.json()

        if "results" not in data:
            raise RuntimeError(f"Polygon error: {data}")

        return {
            "symbol": symbol,
            "price": float(data["results"][0]["c"])
        }

    # ===== FOREX (TwelveData) =====
    td_symbol = TWELVE_SYMBOL_MAP.get(symbol)

    if not td_symbol:
        raise RuntimeError(f"Unsupported TwelveData symbol: {symbol}")

    url = (
        "https://api.twelvedata.com/price?"
        f"symbol={td_symbol}&apikey={TWELVE_API_KEY}"
    )

    r = requests.get(url, timeout=10)
    data = r.json()

    if "price" not in data:
        raise RuntimeError(f"TwelveData error for {symbol}: {data}")

    return {
        "symbol": symbol,
        "price": float(data["price"])
    }
