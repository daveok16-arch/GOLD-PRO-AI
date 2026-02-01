from signal_engine import generate_signal
from notifier import send_signal

SYMBOLS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]

for s in SYMBOLS:
    data = generate_signal(s)

    if data.get("signal") in ["BUY", "SELL"] and data.get("confidence", 0) >= 90:
        send_signal(data)
        print(f"[SENT] {data['symbol']} {data['signal']} @ {data['price']}")
    else:
        print(f"[SKIP] {s}")
