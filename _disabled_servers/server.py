from app import app

# ---- FIX: register routes BEFORE running ----

from analytics import time_of_day_analytics, best_trading_hour
from storage import load_signals

@app.route("/analytics/time")
def analytics_time_api():
    signals = load_signals()
    return {"by_hour": time_of_day_analytics(signals)}

@app.route("/analytics/best-hour")
def analytics_best_hour_api():
    signals = load_signals()
    return best_trading_hour(signals)

# ---- RUN SERVER ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

# ---- REGISTER PERFORMANCE V2 ----
try:
    from register_performance import register
    register(app)
except Exception as e:
    print("[REGISTER PERF V2 server.py]", e)

# ---- EXPECTANCY LEADERBOARD ----
try:
    from analytics import expectancy_leaderboard
    from storage import load_signals

    @app.route("/analytics/expectancy")
    def analytics_expectancy():
        return {"leaderboard": expectancy_leaderboard(load_signals())}

except Exception as e:
    print("[EXPECTANCY ROUTE ERROR]", e)
