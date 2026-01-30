import numpy as np
from tensorflow.keras.models import load_model
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
import logging
from data_fetcher import DataFetcher
import config

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO)

class SignalGenerator:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.sia = SentimentIntensityAnalyzer()
        self.newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
        self.models = {sym: load_model(f"{sym}_{config.MODEL_PATH}") for sym in config.SYMBOLS.keys() if os.path.exists(f"{sym}_{config.MODEL_PATH}")}

    def get_sentiment(self, keyword):
        try:
            articles = self.newsapi.get_everything(q=keyword, language="en", sort_by="relevancy", page_size=10)
            sentiments = [self.sia.polarity_scores(a["title"])["compound"] for a in articles["articles"]]
            return np.mean(sentiments) if sentiments else 0
        except Exception as e:
            logging.error(f"Sentiment failed for {keyword}: {e}")
            return 0

    def generate_signal(self, symbol_key):
        symbol = config.SYMBOLS[symbol_key]
        df = self.fetcher.fetch_latest(symbol)
        if df.empty:
            return "NO_DATA", 0

        # Technical indicators
        rsi_df = self.fetcher.fetch_indicator(symbol, "rsi")
        macd_df = self.fetcher.fetch_indicator(symbol, "macd")
        rsi = rsi_df["rsi"].iloc[0] if not rsi_df.empty else 50
        macd = macd_df["macd"].iloc[0] if not macd_df.empty else 0

        # AI prediction
        if symbol_key in self.models:
            last_seq = df["close"].values[-60:].reshape(1, 60, 1)  # Assume scaler from training
            pred = self.models[symbol_key].predict(last_seq)[0][0]
            ai_signal = "UP" if pred > 0.5 else "DOWN"
        else:
            ai_signal = "NO_MODEL"

        # Sentiment
        sentiment = self.get_sentiment(symbol_key.lower() + " market")

        # Combine: Simple rule-based + AI + sentiment
        score = 0
        if rsi < 30: score += 1  # Oversold
        if rsi > 70: score -= 1  # Overbought
        if macd > 0: score += 1
        if ai_signal == "UP": score += 2
        if sentiment > 0.2: score += 1
        if sentiment < -0.2: score -= 1

        if score > 2: return "BUY", score
        elif score < -2: return "SELL", score
        else: return "HOLD", score

