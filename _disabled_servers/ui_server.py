from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/analytics/ui")
def ui():
    return render_template("analytics.html")

@app.route("/analytics/expectancy")
def expectancy():
    return jsonify({
        "expectancy": 0,
        "wins": 0,
        "losses": 0
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
