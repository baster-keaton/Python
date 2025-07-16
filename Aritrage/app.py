from flask import Flask, jsonify, render_template
from scheduler_module import latest_prices

app = Flask(__name__)

@app.route("/prices")
def prices():
    return jsonify(latest_prices)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", prices=latest_prices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

