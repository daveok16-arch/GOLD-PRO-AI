import requests
from config import POLYGON_API_KEY, TWELVE_API_KEY

def fetch_polygon(symbol, timeframe):
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{timeframe}/"
        f"{get_dates()}?adjusted=true&sort=asc&limit=200&apiKey={POLYGON_API_KEY}"
    )
    r = requests.get(url, timeout=10).json()

    if "results" not in r:
        raise RuntimeError(r.get("error", "Polygon error"))

    return {
        "values": [
            {
                "close": x["c"],
                "open": x["o"],
                "high": x["h"],
                "low": x["l"]
            } for x in r["results"]
        ]
    }

def fetch_twelve(symbol, timeframe):
    url = (
        f"https://api.twelvedata.com/time_series?"
        f"symbol={symbol}&interval={timeframe}&apikey={TWELVE_API_KEY}"
    )
    r = requests.get(url, timeout=10).json()

    if "values" not in r:
        raise RuntimeError(r.get("message", "TwelveData error"))

    return r

def get_dates():
    import datetime
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=5)
    return f"{start.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}"
