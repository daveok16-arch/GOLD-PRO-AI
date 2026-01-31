from config import SYMBOLS, CONFIDENCE_MIN
from data_fetcher import fetch_market_data
from signal_engine import generate_signal
from state import save_signal
import datetime

def run_scan():
    results = []

    for symbol in SYMBOLS:
        try:
            market = fetch_market_data(symbol)
            signal, confidence = generate_signal(symbol, market["price"])

            if confidence < CONFIDENCE_MIN:
                continue

            entry = {
                "symbol": symbol,
                "signal": signal,
                "confidence": confidence,
                "price": market["price"],
                "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }

            save_signal(entry)
            results.append(entry)

        except Exception as e:
            print(f"[WARN] {symbol}: {e}")

    return results
