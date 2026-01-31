from flask import Flask, jsonify, render_template_string
from state import state

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>GOLD-PRO-AI Dashboard</title>
    <meta http-equiv="refresh" content="5">
    < style>
        body { font-family: Arial; background: #0f172a; color: #e5e7eb; padding: 20px; }
        .box { background: #111827; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        h1 { color: #38bdf8; }
    </style>
</head>
<body>
    <h1>🤖 GOLD-PRO-AI Dashboard</h1>

    <div class="box">
        <b>Balance:</b> ${{balance}}<br>
        <b>Last Signal:</b> {{signal}}<br>
        <b>Confidence:</b> {{confidence}}%<br>
        <b>Last Update:</b> {{update}}
    </div>

    <div class="box">
        <h3>📈 Open Trades</h3>
        {% if trades %}
            {% for t in trades %}
                <p>{{t.symbol}} | Entry: {{t.entry}} | Conf: {{t.confidence}}</p>
            {% endfor %}
        {% else %}
            <p>No open trades</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        balance=round(state["balance"], 2),
        signal=state["last_signal"],
        confidence=state["confidence"],
        update=state["last_update"],
        trades=state["open_trades"]
    )

@app.route("/status")
def status():
    return jsonify(state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
