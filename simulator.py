import logging
import config

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO)

class TradeSimulator:
    def __init__(self):
        self.balance = config.ACCOUNT_BALANCE
        self.positions = {sym: 0 for sym in config.SYMBOLS.keys()}

    def execute_trade(self, symbol, action, price):
        if action == "BUY":
            amount = (self.balance * config.RISK_PER_TRADE) / price
            self.positions[symbol] += amount
            self.balance -= amount * price
            logging.info(f"Sim BUY {symbol}: {amount} @ {price}. Bal: {self.balance}")
        elif action == "SELL":
            if self.positions[symbol] > 0:
                amount = self.positions[symbol]
                self.balance += amount * price
                self.positions[symbol] = 0
                logging.info(f"Sim SELL {symbol}: {amount} @ {price}. Bal: {self.balance}")

    def get_portfolio_value(self, prices):
        value = self.balance
        for sym, amt in self.positions.items():
            value += amt * prices.get(sym, 0)
        return value
