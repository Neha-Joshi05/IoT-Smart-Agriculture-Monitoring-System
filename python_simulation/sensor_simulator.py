# ============================================================
# sensor_simulator.py — Virtual Sensor Data Generator
# PURPOSE: Simulates real IoT sensor readings without hardware.
# INTERVIEW TIP: "In real systems, sensors send analog values.
#                 Here we use random + sine wave patterns to
#                 mimic real soil drying / temperature cycles."
# ============================================================

import random
import math
import time
from datetime import datetime

# ── Sensor Threshold Configuration ───────────────────────────
# These are the decision boundaries for automation
THRESHOLDS = {
    "soil_moisture":  {"low": 30, "high": 80},   # % — below 30 → pump ON
    "temperature":    {"low": 10, "high": 38},   # °C — above 38 → fan alert
    "humidity":       {"low": 20, "high": 90},   # % — below 20 → mist alert
    "light_intensity":{"low": 200, "high": 900}, # lux
    "water_level":    {"low": 20, "high": 100},  # % — below 20 → tank alert
}

# ── Simulate sensor reading with realistic noise ──────────────
# time_step drives slow oscillation (like day/night cycle)
def generate_sensor_data(time_step: int) -> dict:
    """
    Generates one reading from all 5 virtual sensors.
    Uses sine wave + noise to mimic realistic patterns.
    """
    # Soil moisture: slowly decreases (drying), occasionally spiked (rain/irrigation)
    base_soil = 55 + 30 * math.sin(time_step / 20)
    soil_moisture = max(5, min(100, base_soil + random.uniform(-5, 5)))

    # Temperature: peaks in afternoon, low at night
    base_temp = 27 + 10 * math.sin(time_step / 15 - 1)
    temperature = round(max(5, min(50, base_temp + random.uniform(-2, 2))), 1)

    # Humidity: inversely related to temperature
    base_hum = 65 - 0.5 * (temperature - 27)
    humidity = round(max(10, min(100, base_hum + random.uniform(-5, 5))), 1)

    # Light: zero at night, peaks midday
    base_light = 500 + 400 * math.sin(time_step / 12)
    light_intensity = max(0, round(base_light + random.uniform(-50, 50)))

    # Water level: slowly drops, refills occasionally
    base_water = 60 + 35 * math.sin(time_step / 30)
    water_level = max(0, min(100, round(base_water + random.uniform(-3, 3))))

    return {
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture":   round(soil_moisture, 1),
        "temperature":     temperature,
        "humidity":        humidity,
        "light_intensity": light_intensity,
        "water_level":     water_level,
    }


def check_alerts(data: dict) -> list:
    alerts = []

    if data["soil_moisture"] < THRESHOLDS["soil_moisture"]["low"]:
        alerts.append("LOW SOIL MOISTURE - Pump should turn ON")
    elif data["soil_moisture"] > THRESHOLDS["soil_moisture"]["high"]:
        alerts.append("Soil moisture is optimal")

    if data["temperature"] > THRESHOLDS["temperature"]["high"]:
        alerts.append(
            f"HIGH TEMPERATURE ({data['temperature']} C) - Enable cooling/fan"
        )

    if data["humidity"] < THRESHOLDS["humidity"]["low"]:
        alerts.append("LOW HUMIDITY - Enable misting system")

    if data["water_level"] < THRESHOLDS["water_level"]["low"]:
        alerts.append("LOW WATER TANK LEVEL - Refill required")

    if data["light_intensity"] < THRESHOLDS["light_intensity"]["low"]:
        alerts.append("LOW LIGHT - Consider grow lights")

    return alerts


def decide_pump(soil_moisture: float) -> str:
    """
    Irrigation decision engine.
    Returns "ON" or "OFF" based on soil moisture level.
    """
    if soil_moisture < THRESHOLDS["soil_moisture"]["low"]:
        return "ON"
    return "OFF"


# ── Standalone test (run this file directly to test) ─────────
if __name__ == "__main__":
    print("=" * 55)
    print("  IoT Smart Agriculture — Sensor Simulation Test")
    print("=" * 55)

    for step in range(10):
        data = generate_sensor_data(step)
        alerts = check_alerts(data)
        pump = decide_pump(data["soil_moisture"])

        print(f"\n[Reading #{step + 1}] {data['timestamp']}")
        print(f"  🌱 Soil Moisture  : {data['soil_moisture']}%")
        print(f"  🌡️  Temperature    : {data['temperature']}°C")
        print(f"  💧 Humidity       : {data['humidity']}%")
        print(f"  ☀️  Light Intensity: {data['light_intensity']} lux")
        print(f"  🪣 Water Level    : {data['water_level']}%")
        print(f"  🚿 Pump Status    : {pump}")

        if alerts:
            print("  ALERTS:")
            for alert in alerts:
                print(f"    → {alert}")
        else:
            print("  ✅ All parameters normal")

        time.sleep(1)