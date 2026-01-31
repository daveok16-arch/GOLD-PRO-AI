import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_signal(symbol, signal, confidence, price):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    message = (
        f"📡 GOLD-PRO-AI SIGNAL\n\n"
        f"Symbol: {symbol}\n"
        f"Signal: {signal}\n"
        f"Confidence: {confidence}%\n"
        f"Price: {price}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
