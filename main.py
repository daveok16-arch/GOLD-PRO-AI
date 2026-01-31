from config import SYMBOLS, TIMEFRAME, CONFIDENCE_MIN
from data_fetcher import fetch_market_data
from signal_engine import generate_signal
from notifier import send_signal
from state import update_signal

print("GOLD-PRO-AI — SIGNAL SCANNER")

for name, cfg in SYMBOLS.items():
    try:
        data = fetch_market_data(cfg, TIMEFRAME)
        closes = data["closes"]

        signal, confidence = generate_signal(closes)

        if signal and confidence >= CONFIDENCE_MIN:
            update_signal(
                symbol=name,
                signal=signal,
                confidence=confidence,
                price=closes[-1]
            )
            send_signal(name, signal, confidence, closes[-1])
            print(f"[SIGNAL] {name}: {signal} ({confidence}%)")
        else:
            print(f"[NO SIGNAL] {name}")

    except Exception as e:
        print(f"[SKIP] {name}: {e}")
