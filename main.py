import time
from datetime import datetime
import pytz
from signal_generator import SignalGenerator
from simulator import TradeSimulator
from notifier import Notifier
from data_fetcher import DataFetcher
import config
import logging

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO)

def main():
    generator = SignalGenerator()
    simulator = TradeSimulator()
    notifier = Notifier()
    fetcher = DataFetcher()
    tz = pytz.timezone(config.TIMEZONE)

    notifier.send_message(f"🤖 *GOLD-PRO-AI Bot* Started\nTime: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')} WAT")

    while True:
        lines = [f"📈 *Market Update* {datetime.now(tz).strftime('%H:%M')}"]
        prices = {}
        for sym_key in config.SYMBOLS.keys():
            df = fetcher.fetch_latest(config.SYMBOLS[sym_key])
            if not df.empty:
                price = df["close"].iloc[0]
                prices[sym_key] = price
                signal, score = generator.generate_signal(sym_key)
                lines.append(f"• {sym_key}: {signal} (Score: {score}) | Price: **{price:.2f}**")
                simulator.execute_trade(sym_key, signal, price)
            else:
                lines.append(f"• {sym_key}: ⚠️ No data")

        portfolio_value = simulator.get_portfolio_value(prices)
        lines.append(f"💰 Sim Portfolio: ${portfolio_value:.2f}")

        notifier.send_message("\n".join(lines))
        logging.info("\n".join(lines))

        time.sleep(config.CHECK_EVERY_SECONDS)

if __name__ == "__main__":
    main()
