import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env if you prefer secrets there

TWELVE_API_KEY = "083054b70e074f92b64ebdc75e084f4c"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY_HERE"  # Replace with your key from newsapi.org

SYMBOLS = {
    "GOLD": "XAU/USD",
    "BITCOIN": "BTC/USD",
    "VIX": "VIX",
    "SPX": "SPX",
    "NDX": "NDX"
}

TELEGRAM_BOT_TOKEN = "8214823027:AAHVfjk9KxRGGlS9svqKaiw4Qg0DFhx0o-8"
TELEGRAM_CHAT_ID = "7779937295"

INTERVAL = "5min"
HISTORICAL_DAYS = 365  # For training
OUTPUT_SIZE = 200  # Bars for analysis

MODEL_PATH = "lstm_model.h5"
LOG_FILE = "bot.log"

# Risk management
RISK_PER_TRADE = 0.01  # 1% of account
ACCOUNT_BALANCE = 10000  # Simulated

TIMEZONE = "Africa/Lagos"
