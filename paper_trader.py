import datetime

class PaperTrader:
    def __init__(self, starting_balance=10000):
        self.balance = starting_balance
        self.open_trades = []
        self.trade_log = []
        self.today = datetime.date.today()
        self.trades_today = 0

    def reset_daily_counter(self):
        if datetime.date.today() != self.today:
            self.today = datetime.date.today()
            self.trades_today = 0

    def can_trade(self, max_trades):
        self.reset_daily_counter()
        return self.trades_today < max_trades

    def open_trade(self, symbol, direction, confidence, price):
        trade = {
            "symbol": symbol,
            "direction": direction,
            "entry": price,
            "confidence": confidence,
            "opened": datetime.datetime.utcnow()
        }
        self.open_trades.append(trade)
        self.trades_today += 1
        return trade

    def close_trade(self, trade, exit_price, reason):
        pnl = (
            exit_price - trade["entry"]
            if trade["direction"] == "BUY"
            else trade["entry"] - exit_price
        )

        self.balance += pnl

        trade["exit"] = exit_price
        trade["pnl"] = pnl
        trade["reason"] = reason
        trade["closed"] = datetime.datetime.utcnow()

        self.trade_log.append(trade)
        self.open_trades.remove(trade)

        return trade

    def check_exits(self, current_price, tp_pct, sl_pct, max_minutes):
        closed = []
        now = datetime.datetime.utcnow()

        for trade in self.open_trades[:]:
            entry = trade["entry"]
            age = (now - trade["opened"]).total_seconds() / 60

            tp = entry * (1 + tp_pct)
            sl = entry * (1 - sl_pct)

            if current_price >= tp:
                closed.append(self.close_trade(trade, current_price, "TAKE_PROFIT"))

            elif current_price <= sl:
                closed.append(self.close_trade(trade, current_price, "STOP_LOSS"))

            elif age >= max_minutes:
                closed.append(self.close_trade(trade, current_price, "TIME_EXIT"))

        return closed
