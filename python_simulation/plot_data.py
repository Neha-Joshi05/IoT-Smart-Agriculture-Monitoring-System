# ============================================================
# plot_data.py — Offline Chart Generator from CSV
# PURPOSE: Generates PNG charts from logged sensor data.
# HOW TO RUN: python python_simulation/plot_data.py
# ============================================================

import csv
import os

def plot_sensor_data():
    """
    Reads sensor_log.csv and prints an ASCII trend chart.
    Also works as a fallback when matplotlib is not installed.
    """
    log_file = "data/sensor_log.csv"

    if not os.path.exists(log_file):
        print("❌ No log file found. Run main.py first.")
        return

    rows = []
    with open(log_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("❌ Log file is empty.")
        return

    print("\n" + "=" * 60)
    print("  📊 Sensor Data Summary Report")
    print("=" * 60)
    print(f"  Total readings: {len(rows)}")
    print(f"  First reading : {rows[0]['timestamp']}")
    print(f"  Last reading  : {rows[-1]['timestamp']}")

    # ── Calculate averages ────────────────────────────────────
    fields = ["soil_moisture", "temperature", "humidity", "light_intensity", "water_level"]
    labels = {
        "soil_moisture":   "🌱 Avg Soil Moisture",
        "temperature":     "🌡️  Avg Temperature",
        "humidity":        "💧 Avg Humidity",
        "light_intensity": "☀️  Avg Light",
        "water_level":     "🪣 Avg Water Level"
    }

    print("\n  ── Averages ─────────────────────────")
    for field in fields:
        values = [float(r[field]) for r in rows if r[field]]
        avg = sum(values) / len(values) if values else 0
        print(f"  {labels[field]:30s}: {avg:.1f}")

    # ── Pump statistics ───────────────────────────────────────
    pump_on  = sum(1 for r in rows if r["pump_status"] == "ON")
    pump_off = len(rows) - pump_on
    print(f"\n  ── Pump Activity ────────────────────")
    print(f"  🚿 Pump ON  count : {pump_on}")
    print(f"  ⏹️  Pump OFF count : {pump_off}")
    print(f"  📊 Irrigation rate : {pump_on/len(rows)*100:.1f}%")

    # ── ASCII trend for soil moisture ─────────────────────────
    print("\n  ── Soil Moisture Trend (last 20 readings) ──")
    recent = rows[-20:]
    for r in recent:
        val = float(r["soil_moisture"])
        bar_len = int(val / 5)
        bar = "█" * bar_len
        status = "DRY🚨" if val < 30 else "OK ✅"
        print(f"  {val:5.1f}% |{bar:<20}| {status}")

    print("\n✅ Report complete. Check data/sensor_log.csv for full data.\n")


if __name__ == "__main__":
    plot_sensor_data()