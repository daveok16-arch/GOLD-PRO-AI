from config import SYMBOLS, CONFIDENCE_MIN
from data_fetcher import fetch_market_data
from signal_engine import generate_signal
from state import save_signal

def run_scan():
    results = []

    for symbol in SYMBOLS:
        try:
            market = fetch_market_data(symbol, timeframe=None)
            signal = generate_signal(symbol, market["price"])

            if signal["confidence"] >= CONFIDENCE_MIN:
                save_signal(signal)
                results.append(signal)

        except Exception as e:
            print(f"[WARN] {symbol}: {e}")

    return results
