def ema(prices, period):
    if len(prices) < period:
        return prices[-1]

    k = 2 / (period + 1)
    ema_val = prices[0]
    for price in prices[1:]:
        ema_val = price * k + ema_val * (1 - k)
    return round(ema_val, 5)


def rsi(prices, period=14):
    if len(prices) <= period:
        return 50.0

    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period if sum(losses[-period:]) != 0 else 1

    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)
