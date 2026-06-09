# ============================================================
# dashboard/app.py — Real-Time Web Dashboard (Flask)
# PURPOSE: Serves a live dashboard showing sensor data.
# HOW TO RUN locally : python dashboard/app.py
# HOW TO DEPLOY      : Render / Railway reads PORT from environment
# ============================================================

import sys
import os

# Add parent folder to path so we can import our simulation modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, jsonify
from python_simulation.sensor_simulator import (
    generate_sensor_data, check_alerts, decide_pump
)
from python_simulation.data_logger import init_logger, log_reading, get_recent_logs
import threading
import time

app = Flask(__name__)

# ── Shared state ──────────────────────────────────────────────
latest_data   = {}
latest_pump   = "OFF"
latest_alerts = []
data_lock     = threading.Lock()
step_counter  = [0]


# ── Background sensor simulation thread ──────────────────────
def background_simulator():
    init_logger()
    while True:
        step_counter[0] += 1
        data   = generate_sensor_data(step_counter[0])
        alerts = check_alerts(data)
        pump   = decide_pump(data["soil_moisture"])

        log_reading(data, pump, alerts)

        with data_lock:
            latest_data.update(data)
            latest_alerts[:] = alerts

        # global needed to reassign a string variable from inside a function
        global latest_pump
        latest_pump = pump

        time.sleep(3)


# ── Routes ────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/latest")
def api_latest():
    with data_lock:
        return jsonify({
            "data":   dict(latest_data),
            "pump":   latest_pump,
            "alerts": list(latest_alerts),
        })


@app.route("/api/history")
def api_history():
    rows = get_recent_logs(50)
    return jsonify(rows)


# ── Start background thread ───────────────────────────────────
# daemon=True means thread stops automatically when app stops
t = threading.Thread(target=background_simulator, daemon=True)
t.start()


# ── Start server ──────────────────────────────────────────────
# KEY CHANGE: os.environ.get("PORT", 5000)
# WHY: Render assigns a random PORT at runtime via environment variable.
#      If we hardcode 5000, Render cannot reach our app and deployment fails.
#      Locally, PORT is not set, so it falls back to 5000 automatically.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)