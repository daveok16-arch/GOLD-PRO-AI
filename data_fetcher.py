import os
import requests

API_KEY = os.getenv("TWELVE_API_KEY")

def fetch_market_data(symbol, interval):
    if not API_KEY:
        raise RuntimeError("TWELVE_API_KEY not set")

    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY,
        "outputsize": 100
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    # Defensive checks
    if "status" in data and data["status"] == "error":
        raise RuntimeError(f"TwelveData error for {symbol}: {data.get('message')}")

    if "values" not in data or not data["values"]:
        raise RuntimeError(f"No candle data returned for {symbol}")

    return data
