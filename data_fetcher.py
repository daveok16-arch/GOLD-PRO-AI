import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import pytz
import config

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFetcher:
    def __init__(self):
        self.base_url = "https://api.twelvedata.com"
        self.tz = pytz.timezone(config.TIMEZONE)

    def fetch_historical(self, symbol, days=config.HISTORICAL_DAYS):
        end_date = datetime.now(self.tz).strftime("%Y-%m-%d")
        start_date = (datetime.now(self.tz) - timedelta(days=days)).strftime("%Y-%m-%d")
        params = {
            "symbol": symbol,
            "interval": config.INTERVAL,
            "start_date": start_date,
            "end_date": end_date,
            "outputsize": 5000,  # Max for history
            "apikey": config.TWELVE_API_KEY
        }
        try:
            r = requests.get(f"{self.base_url}/time_series", params=params)
            r.raise_for_status()
            data = r.json()["values"]
            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df.set_index("datetime", inplace=True)
            df = df.astype(float)
            logging.info(f"Fetched historical for {symbol}")
            return df
        except Exception as e:
            logging.error(f"Fetch historical failed for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_latest(self, symbol):
        params = {
            "symbol": symbol,
            "interval": config.INTERVAL,
            "outputsize": config.OUTPUT_SIZE,
            "apikey": config.TWELVE_API_KEY
        }
        try:
            r = requests.get(f"{self.base_url}/time_series", params=params)
            r.raise_for_status()
            data = r.json()["values"]
            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df.set_index("datetime", inplace=True)
            df = df.astype(float)
            return df
        except Exception as e:
            logging.error(f"Fetch latest failed for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_indicator(self, symbol, indicator="rsi", period=14):
        params = {
            "symbol": symbol,
            "interval": config.INTERVAL,
            "indicator": indicator,
            "time_period": period,
            "outputsize": config.OUTPUT_SIZE,
            "apikey": config.TWELVE_API_KEY
        }
        try:
            r = requests.get(f"{self.base_url}/technical_indicators", params=params)
            r.raise_for_status()
            data = r.json()["values"]
            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df.set_index("datetime", inplace=True)
            df = df.astype(float)
            return df
        except Exception as e:
            logging.error(f"Indicator {indicator} failed for {symbol}: {e}")
            return pd.DataFrame()
