from trade_resolver import resolve_trades
from flask import Flask, jsonify
from analytics import (
    build_analytics,
    best_performing_symbols,
    time_of_day_analytics,
    expectancy
)
from storage import load_signals

app = Flask(__name__)

@app.route("/analytics")
def analytics_api():
    return jsonify(build_analytics())

@app.route("/analytics/ranking")
def analytics_ranking():
    return jsonify({
        "best_performing": best_performing_symbols()
    })

@app.route("/analytics/time")
def analytics_time():
    signals = load_signals()
    return jsonify({
        "by_hour": time_of_day_analytics(signals)
    })

@app.route("/analytics/expectancy")
def analytics_expectancy():
    signals = load_signals()
    return jsonify(expectancy(signals))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)

from analytics_performance import performance_from_signals, best_trading_hour
from storage import load_signals

@app.route("/analytics/performance")
def analytics_performance():
    signals = load_signals()
    return performance_from_signals(signals)

@app.route("/analytics/best-hour")
def analytics_best_hour():
    signals = load_signals()
    return {"best_hour": best_trading_hour(signals)}
