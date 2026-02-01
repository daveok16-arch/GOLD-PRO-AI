from flask import jsonify
from analytics import performance_metrics
from storage import load_signals

def register_performance_routes(app):

    @app.route("/analytics/performance")
    def analytics_performance():
        signals = load_signals()
        return jsonify(performance_metrics(signals))
