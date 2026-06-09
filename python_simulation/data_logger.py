import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "..", "data", "sensor_log.csv")

HEADERS = [
    "timestamp", "soil_moisture", "temperature",
    "humidity", "light_intensity", "water_level",
    "pump_status", "alerts"
]

def init_logger():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()

def log_reading(data, pump_status, alerts):
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
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)

def get_recent_logs(n=50):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows[-n:]