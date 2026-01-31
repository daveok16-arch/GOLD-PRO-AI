def tradingview_chart(symbol):
    """
    Returns TradingView chart URL for a symbol
    """

    if symbol == "XAUUSD":
        return "https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD"

    # Forex pairs
    return f"https://www.tradingview.com/chart/?symbol=FX:{symbol}"
