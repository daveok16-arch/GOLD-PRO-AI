import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_signal(data):
    message = f"""
<b>{data['symbol']} TRADE SIGNAL</b>

<ul>
<li><b>Direction:</b> {data['signal']}</li>
<li><b>Confidence:</b> {data['confidence']}%</li>
<li><b>Trend:</b> {data['trend']}</li>
<li><b>Entry:</b> {data['price']}</li>
<li><b>Stop Loss:</b> {data['SL']}</li>
<li><b>Take Profit:</b> {data['TP']}</li>
<li><b>RSI:</b> {data['rsi']}</li>
<li><b>Model:</b> {data['model']}</li>
</ul>

<i>London / NY Smart Money Execution</i>
"""

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    r = requests.post(TELEGRAM_URL, json=payload, timeout=10)
    r.raise_for_status()
