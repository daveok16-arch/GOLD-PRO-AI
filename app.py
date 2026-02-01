import os
from flask import render_template
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


# from analytics_performance import performance_from_signals, best_trading_hour
from storage import load_signals

@app.route("/analytics/performance")
def analytics_performance():
    signals = load_signals()
    return performance_from_signals(signals)

@app.route("/analytics/best-hour")
def analytics_best_hour():
    signals = load_signals()
    return {"best_hour": best_trading_hour(signals)}

from flask import render_template

@app.route("/analytics-ui")
def analytics_ui():
    return render_template("analytics.html")

@app.route("/api/analytics/summary")
def analytics_summary():
    return {
        "equity": [10000,10050,10120,10080,10230,10310],
        "wins": 18,
        "losses": 7
    }

from flask import render_template

def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/")
def home():
    return render_template("analytics.html")

@app.route("/", endpoint="home_root")
def home_root():
    return render_template("analytics.html")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), debug=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), debug=False)
