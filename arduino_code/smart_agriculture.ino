// ============================================================
// smart_agriculture.ino — ESP32 Firmware
// PURPOSE: Real hardware code for ESP32 + sensors + MQTT.
// INTERVIEW TIP: "This is the embedded side — the MCU reads
//                 sensors via ADC/I2C and publishes JSON over MQTT."
// NOTE: Use Wokwi.com to simulate this without hardware.
//       Wokwi supports ESP32 + DHT22 + soil sensor.
// ============================================================

#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// ── Pin Configuration ─────────────────────────────────────────
#define DHTPIN        4    // DHT22 data pin
#define DHTTYPE       DHT22
#define SOIL_PIN      34   // Analog soil moisture sensor
#define LDR_PIN       35   // Analog LDR (light sensor)
#define WATER_PIN     32   // Analog water level sensor
#define RELAY_PIN     25   // Relay IN (LOW = pump ON)

// ── Network + MQTT Configuration ─────────────────────────────
// IMPORTANT: Move these to a config.h file — never commit secrets
const char* WIFI_SSID   = "YOUR_WIFI_SSID";
const char* WIFI_PASS   = "YOUR_WIFI_PASSWORD";
const char* MQTT_SERVER = "broker.hivemq.com";   // free public broker
const int   MQTT_PORT   = 1883;

// ── Thresholds ────────────────────────────────────────────────
// Soil moisture ADC: 0 = wet, 4095 = dry (inverted scale)
// Map raw ADC to 0-100% moisture
const int SOIL_DRY_THRESHOLD = 2500;   // below this → pump ON

// ── Object Initialization ─────────────────────────────────────
DHT          dht(DHTPIN, DHTTYPE);
WiFiClient   espClient;
PubSubClient mqtt(espClient);

// ── Setup ─────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial.println("\n🌾 Smart Agriculture System Starting...");

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // HIGH = pump OFF (active-low relay)

  dht.begin();

  // Connect WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Connected: " + WiFi.localIP().toString());

  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
  Serial.println("🔌 MQTT Configured");
}

// ── MQTT Reconnect ────────────────────────────────────────────
void reconnectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect("SmartFarmNode_001")) {
      Serial.println(" Connected!");
    } else {
      Serial.print(" Failed, rc=");
      Serial.println(mqtt.state());
      delay(3000);
    }
  }
}

// ── Read + Map Sensors ────────────────────────────────────────
int readSoilMoisture() {
  int raw = analogRead(SOIL_PIN);
  // Map ADC (0-4095) to percentage (0-100%)
  // Capacitive sensor: high raw = dry, low raw = wet
  return map(raw, 4095, 0, 0, 100);
}

int readLightIntensity() {
  int raw = analogRead(LDR_PIN);
  // Map to approximate lux (0-1000)
  return map(raw, 0, 4095, 0, 1000);
}

int readWaterLevel() {
  int raw = analogRead(WATER_PIN);
  return map(raw, 0, 4095, 0, 100);
}

// ── Irrigation Decision ───────────────────────────────────────
void controlPump(int soilMoisture) {
  if (soilMoisture < 30) {
    // Soil is dry → turn pump ON
    digitalWrite(RELAY_PIN, LOW);
    mqtt.publish("farm/node1/pump", "ON");
    Serial.println("🚿 PUMP ON — Soil dry");
  } else {
    // Soil is adequate → pump OFF
    digitalWrite(RELAY_PIN, HIGH);
    mqtt.publish("farm/node1/pump", "OFF");
  }
}

// ── Main Loop ─────────────────────────────────────────────────
void loop() {
  if (!mqtt.connected()) reconnectMQTT();
  mqtt.loop(); // keeps MQTT connection alive

  // Read all sensors
  float temperature = dht.readTemperature();
  float humidity    = dht.readHumidity();
  int soilMoisture  = readSoilMoisture();
  int lightIntensity = readLightIntensity();
  int waterLevel    = readWaterLevel();

  // Check for failed DHT reading
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("⚠️ DHT read failed — using defaults");
    temperature = 25.0;
    humidity    = 60.0;
  }

  // Build JSON payload
  // WHY: MQTT payloads are typically JSON strings for easy parsing
  char payload[256];
  snprintf(payload, sizeof(payload),
    "{\"temp\":%.1f,\"hum\":%.1f,\"soil\":%d,\"light\":%d,\"water\":%d}",
    temperature, humidity, soilMoisture, lightIntensity, waterLevel
  );

  // Publish sensor data to MQTT topic
  mqtt.publish("farm/node1/data", payload);

  // Print to Serial Monitor (useful for debugging)
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  Serial.printf("🌡️  Temp: %.1f°C | 💧 Hum: %.1f%%\n", temperature, humidity);
  Serial.printf("🌱 Soil: %d%% | ☀️  Light: %d lux | 🪣 Water: %d%%\n",
                soilMoisture, lightIntensity, waterLevel);
  Serial.printf("📡 Published: %s\n", payload);

  // Make irrigation decision
  controlPump(soilMoisture);

  // Wait 5 seconds before next reading
  delay(5000);
}