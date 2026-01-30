import requests
import time
from datetime import datetime
import config

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Telegram failed: {e}")

def fetch_latest_bars(symbol):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": config.INTERVAL,
        "outputsize": config.OUTPUT_SIZE,
        "apikey": config.TWELVE_API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "ok":
            return data.get("values", [])
        else:
            print(f"API error for {symbol}: {data.get('message', data)}")
            return []
    except Exception as e:
        print(f"Request failed for {symbol}: {e}")
        return []

def get_momentum_signal(bars):
    if len(bars) < 3:
        return "NO_DATA", "N/A"
    closes = [float(b["close"]) for b in bars[:3]]  # last 3 closes
    if closes[0] > closes[1] > closes[2]:
        return "STRONG_UP", closes[0]
    elif closes[0] > closes[1]:
        return "UP", closes[0]
    elif closes[0] < closes[1] < closes[2]:
        return "STRONG_DOWN", closes[0]
    elif closes[0] < closes[1]:
        return "DOWN", closes[0]
    else:
        return "FLAT", closes[0]

# Main loop
send_telegram_message(f"🤖 *GOLD-PRO-AI Bot* started\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WAT\nSymbols: {', '.join(config.SYMBOLS)}")

while True:
    lines = [f"📈 *Update* {datetime.now().strftime('%H:%M')} ({config.INTERVAL})"]
    any_data = False

    for sym in config.SYMBOLS:
        bars = fetch_latest_bars(sym)
        if bars:
            signal, price = get_momentum_signal(bars)
            lines.append(f"• {sym}: {signal} | Price: **{price:.2f}**")
            any_data = True
        else:
            lines.append(f"• {sym}: ⚠️ No data / error")

    if any_data:
        msg = "\n".join(lines)
        send_telegram_message(msg)
        print(msg)
    else:
        print("All fetches failed – check API key / internet / rate limits")

    time.sleep(config.CHECK_EVERY_SECONDS)
