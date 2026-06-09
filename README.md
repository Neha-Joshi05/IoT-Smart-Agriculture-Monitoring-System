# 🌾 IoT-Enabled Smart Agriculture Monitoring System

## 🌐 Live Demo → https://iot-smart-agriculture-monitoring-system.onrender.com

> A Python-based simulation of an IoT smart farming system that monitors soil moisture, temperature, humidity, light intensity, and water level — with automated irrigation control and a live web dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![IoT](https://img.shields.io/badge/IoT-Simulation-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 🎯 Problem Statement

Traditional farming relies on manual observation and guesswork for irrigation decisions. This leads to overwatering (waste), underwatering (crop damage), and missed alerts (crop loss). This IoT system automates monitoring and decision-making in real time.

---

## ✨ Features

- 🌱 **5-Sensor Simulation** — Soil moisture, temperature, humidity, light, water level
- 🚿 **Automated Pump Control** — Turns ON/OFF based on soil moisture threshold
- 📊 **Live Web Dashboard** — Real-time charts + sensor cards (Flask + Chart.js)
- ⚡ **Alert System** — Notifies for dry soil, high temp, low water
- 📁 **CSV Data Logging** — All readings saved for analysis
- 💻 **No Hardware Needed** — Full Python simulation

---

## 🛠️ Tech Stack

| Layer        | Technology                    |
|--------------|-------------------------------|
| Simulation   | Python 3, Math, Threading     |
| Web Server   | Flask                         |
| Frontend     | HTML, CSS, Chart.js           |
| Data Storage | CSV (expandable to DB)        |
| MCU (real)   | ESP32 + Arduino IDE           |
| Protocol     | MQTT (PubSubClient)           |
| Dashboard    | Blynk / ThingSpeak / Node-RED |

---

## 📁 Folder Structure

```
IoT-Smart-Agriculture-Monitoring-System/
├── arduino_code/
│   └── smart_agriculture.ino    ← ESP32 firmware (real hardware)
├── python_simulation/
│   ├── sensor_simulator.py      ← Virtual sensor + alert logic
│   ├── data_logger.py           ← CSV logging module
│   └── plot_data.py             ← Offline data report
├── dashboard/
│   ├── app.py                   ← Flask web server
│   └── templates/
│       └── index.html           ← Live dashboard UI
├── data/
│   └── sensor_log.csv           ← Auto-generated log file
├── outputs/                     ← Screenshots to upload
├── docs/                        ← Architecture diagrams
├── main.py                      ← Terminal simulation runner
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Clone & Install
```bash
git clone https://github.com/Neha-Joshi05/IoT-Smart-Agriculture-Monitoring-System.git
cd IoT-Smart-Agriculture-Monitoring-System
pip install -r requirements.txt
```

### 2. Run Terminal Simulation
```bash
python main.py
```
Outputs live sensor readings + pump status to terminal. Saves to `data/sensor_log.csv`.

### 3. Run Live Dashboard
```bash
python dashboard/app.py
```
Open **http://localhost:5000** in your browser.

### 4. View Data Report
```bash
python python_simulation/plot_data.py
```

---

## 🏗️ Architecture

```
[Virtual Sensors] → [sensor_simulator.py]
        ↓
[Threshold Engine] → [Pump ON/OFF Decision]
        ↓
[data_logger.py]  → [sensor_log.csv]
        ↓
[Flask API]       → [Live Dashboard (Chart.js)]
        ↓
[Alerts]          → [Browser / Console]
```

Real hardware flow:
```
[DHT22 / Soil / LDR] → [ESP32 ADC] → [MQTT Broker]
        → [Node-RED / Blynk Dashboard] → [Relay / Pump]
```

---

## 📊 Sample Output

```
[0001] 2024-01-15 10:32:01
       Soil: 24.5% | Temp: 36.2°C | Hum: 58.1% | Light: 823 lux | Water: 18% | Pump: ON
       🚨 LOW SOIL MOISTURE — Pump should turn ON
       🌡️ HIGH TEMPERATURE (36.2°C) — Enable cooling/fan
       ⚠️ LOW WATER TANK LEVEL — Refill required
```

---

## 🎓 Learning Outcomes

- IoT sensor data flow (sensor → MCU → cloud → dashboard)
- Threshold-based automation and rule engines
- Python threading for concurrent simulation
- Flask REST API design
- Real-time browser updates (polling)
- CSV data logging and analysis
- MQTT protocol for IoT messaging
- ESP32 firmware programming

---
## NEHA JOSHI ##

GIT URL: https://github.com/Neha-Joshi05/IoT-Smart-Agriculture-Monitoring-System.git

LINKEDIN : https://www.linkedin.com/in/neha-joshi-0851a2322?utm_source=share_via&utm_content=profile&utm_medium=member_android
---

