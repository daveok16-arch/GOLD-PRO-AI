from flask import jsonify
from analytics import performance_metrics
from storage import load_signals

def register_performance_fix(app):

    @app.route("/analytics/performance_v2", endpoint="analytics_performance_v2")
    def analytics_performance_v2():
        signals = load_signals()
        return jsonify(performance_metrics(signals))
