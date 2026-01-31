import time
import datetime

from config import (
    SYMBOLS,
    TIMEFRAME,
    SLEEP_SECONDS,
    CONFIDENCE_THRESHOLD,
    MAX_TRADES_PER_DAY,
    STARTING_BALANCE,
    TAKE_PROFIT_PCT,
    STOP_LOSS_PCT,
    MAX_TRADE_MINUTES
)

from data_fetcher import fetch_market_data
from signal_engine import simple_trend_check, generate_signal
from paper_trader import PaperTrader
from notifier import send_telegram
from state import state

# =============================
# INIT
# =============================
trader = PaperTrader(STARTING_BALANCE)

print("GOLD-PRO-AI — PAPER MODE WITH AUTO EXIT")

# =============================
# HELPERS
# =============================
def get_latest_price(data):
    try:
        return float(data["values"][0]["close"])
    except Exception:
        return None

# =============================
# MAIN LOOP
# =============================
def run_cycle():
    market_trends = {}
    prices = {}

    # -------- FETCH & ANALYZE --------
    for key, symbol in SYMBOLS.items():
        try:
            data = fetch_market_data(symbol, TIMEFRAME)
            trend = simple_trend_check(data)
            price = get_latest_price(data)

            if trend and price:
                market_trends[key] = trend
                prices[key] = price

        except Exception as e:
            print(f"[WARN] {symbol}: {e}")

    # -------- AUTO CLOSE TRADES --------
    for trade in trader.open_trades[:]:
        symbol = trade["symbol"]
        price = prices.get(symbol)

        if not price:
            continue

        closed_trades = trader.check_exits(
            current_price=price,
            tp_pct=TAKE_PROFIT_PCT,
            sl_pct=STOP_LOSS_PCT,
            max_minutes=MAX_TRADE_MINUTES
        )

        for t in closed_trades:
            msg = (
                "❌ PAPER TRADE CLOSED\n"
                f"SYMBOL: {t['symbol']}\n"
                f"REASON: {t['reason']}\n"
                f"PNL: {t['pnl']:.2f}\n"
                f"BALANCE: {trader.balance:.2f}"
            )
            print(msg)
            send_telegram(msg)

    # -------- GENERATE SIGNAL --------
    signal, confidence = generate_signal(market_trends)

    # -------- OPEN NEW TRADE --------
    if (
        signal != "NO_TRADE"
        and confidence >= CONFIDENCE_THRESHOLD
        and trader.can_trade(MAX_TRADES_PER_DAY)
    ):
        asset = signal.split("_")[-1]
        price = prices.get(asset)

        if price:
            trade = trader.open_trade(
                symbol=asset,
                direction="BUY",
                confidence=confidence,
                price=price
            )

            msg = (
                "📈 PAPER TRADE OPENED\n"
                f"SYMBOL: {asset}\n"
                f"ENTRY: {price}\n"
                f"CONFIDENCE: {confidence}%"
            )
            print(msg)
            send_telegram(msg)

    # -------- UPDATE DASHBOARD STATE --------
    state["balance"] = round(trader.balance, 2)
    state["open_trades"] = trader.open_trades
    state["last_signal"] = signal
    state["confidence"] = confidence
    state["last_update"] = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

# =============================
# RUN FOREVER
# =============================
if __name__ == "__main__":
    while True:
        run_cycle()
        time.sleep(SLEEP_SECONDS)
