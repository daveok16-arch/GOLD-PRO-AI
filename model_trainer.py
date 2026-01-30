import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import logging
from data_fetcher import DataFetcher
import config

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO)

class ModelTrainer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None

    def prepare_data(self, df, seq_length=60):
        data = self.scaler.fit_transform(df[["close"]])
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i, 0])
            y.append(1 if data[i, 0] > data[i-1, 0] else 0)  # 1=up, 0=down
        return np.array(X), np.array(y)

    def build_model(self, input_shape):
        self.model = Sequential()
        self.model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(50, return_sequences=False))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(1, activation="sigmoid"))
        self.model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        return self.model

    def train(self, symbol):
        fetcher = DataFetcher()
        df = fetcher.fetch_historical(config.SYMBOLS[symbol])
        if df.empty:
            return
        df = df[["close"]].dropna()
        X, y = self.prepare_data(df)
        X = X.reshape(X.shape[0], X.shape[1], 1)
        self.build_model((X.shape[1], 1))
        self.model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)
        self.model.save(f"{symbol}_{config.MODEL_PATH}")
        logging.info(f"Trained model for {symbol}")

if __name__ == "__main__":
    trainer = ModelTrainer()
    for sym in config.SYMBOLS.keys():
        trainer.train(sym)
