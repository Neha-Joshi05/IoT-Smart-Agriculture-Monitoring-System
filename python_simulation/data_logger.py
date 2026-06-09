# ============================================================
# data_logger.py — CSV Data Logging Module
# PURPOSE: Saves every sensor reading to a CSV file.
# INTERVIEW TIP: "Data logging is essential in IoT for auditing,
#                 analytics, and training ML models later."
# ============================================================

import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "..", "data", "sensor_log.csv")

# CSV column headers
HEADERS = [
    "timestamp", "soil_moisture", "temperature",
    "humidity", "light_intensity", "water_level",
    "pump_status", "alerts"
]


def init_logger():
    """
    Creates the CSV file with headers if it doesn't exist.
    WHY: We don't want to overwrite existing data on restart.
    """
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
        print(f"✅ Log file created: {LOG_FILE}")


def log_reading(data: dict, pump_status: str, alerts: list):
    """
    Appends one row to the CSV log.
    Each call = one sensor reading saved permanently.
    """
    row = {
        "timestamp":       data["timestamp"],
        "soil_moisture":   data["soil_moisture"],
        "temperature":     data["temperature"],
        "humidity":        data["humidity"],
        "light_intensity": data["light_intensity"],
        "water_level":     data["water_level"],
        "pump_status":     pump_status,
        "alerts":          " | ".join(alerts) if alerts else "None",
    }

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)


def get_recent_logs(n: int = 50) -> list:
    """
    Reads last N rows from CSV for dashboard display.
    WHY: We only send recent data to avoid overloading the browser.
    """
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return rows[-n:]  # last N readings