# ============================================================
# main.py — Main Entry Point (Simulation Runner)
# PURPOSE: Runs continuous sensor simulation + data logging.
#          Run this in terminal to simulate the IoT system.
# HOW TO RUN: python main.py
# ============================================================

import time
from python_simulation.sensor_simulator import (
    generate_sensor_data, check_alerts, decide_pump
)
from python_simulation.data_logger import init_logger, log_reading

def main():
    print("\n" + "=" * 60)
    print("   🌾 IoT Smart Agriculture Monitoring System")
    print("   Running simulation... Press CTRL+C to stop")
    print("=" * 60 + "\n")

    init_logger()  # Create CSV file if it doesn't exist

    step = 0
    try:
        while True:
            step += 1

            # Step 1: Generate sensor data
            data = generate_sensor_data(step)

            # Step 2: Check alerts against thresholds
            alerts = check_alerts(data)

            # Step 3: Make irrigation decision
            pump = decide_pump(data["soil_moisture"])

            # Step 4: Log to CSV
            log_reading(data, pump, alerts)

            # Step 5: Print to terminal (simulates Serial Monitor)
            print(f"[{step:04d}] {data['timestamp']}")
            print(f"       Soil: {data['soil_moisture']}% | "
                  f"Temp: {data['temperature']}°C | "
                  f"Hum: {data['humidity']}% | "
                  f"Light: {data['light_intensity']} lux | "
                  f"Water: {data['water_level']}% | "
                  f"Pump: {pump}")

            if alerts:
                for alert in alerts:
                    print(f"       {alert}")
            print()

            time.sleep(2)  # Read every 2 seconds (simulate 5 min in real IoT)

    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped. Data saved to data/sensor_log.csv")


if __name__ == "__main__":
    main()