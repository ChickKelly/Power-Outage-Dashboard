#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

// ---------------- Wi-Fi Config ----------------
const char* ssid = "HUAWEI-B311-3448";
const char* password = "NYSD THE BOSS";

// ---------------- MQTT Config (HiveMQ Cloud) ----------------
const char* mqtt_server = "21981c8197844bccbd5f2c47fec665be.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "hivemq.webclient.1758713241793";
const char* mqtt_pass = "PNa1q5BGH#o.9n:u6W>r";

WiFiClientSecure espClient;
PubSubClient client(espClient);

// ---------------- RF24 Config ----------------
RF24 radio(17, 5); // CE, CSN
const byte address[6] = "00001";

// ---------------- Hardware Pins ----------------
int buzzer = 12;
int blueled = 13;
int redled  = 32;

float lastVoltage = 0.0;

// ---------------- Station IDs ----------------
// Each station gets a unique ID
String stations[] = {"station1", "station2", "station3"};
int stationIndex = 0;  // ✅ choose which station this device represents

// ---------------- Functions ----------------
void setup_wifi() {
  delay(10);
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected. IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(stations[stationIndex].c_str(), mqtt_user, mqtt_pass)) {
      Serial.println("✅ Connected to HiveMQ Cloud");
    } else {
      Serial.print("❌ failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(buzzer, OUTPUT);
  pinMode(blueled, OUTPUT);
  pinMode(redled, OUTPUT);

  // Initialize nRF24
  if (!radio.begin()) {
    Serial.println("❌ nRF24L01 not detected. Check wiring!");
    while (1);
  }

  radio.openReadingPipe(0, address);
  radio.startListening();
  Serial.println("✅ Receiver ready, waiting for data...");

  // Wi-Fi + MQTT setup
  setup_wifi();

  espClient.setInsecure();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (radio.available()) {
    float voltage;
    radio.read(&voltage, sizeof(voltage));
    lastVoltage = voltage;

    Serial.print("📡 Received Voltage: ");
    Serial.println(voltage);

    // Control outputs
    if (voltage < 1) {
      digitalWrite(blueled, LOW);
      digitalWrite(redled, HIGH);
      tone(buzzer, 1500);
    } else {
      digitalWrite(redled, LOW);
      digitalWrite(blueled, HIGH);
      noTone(buzzer);
    }

    // ---------------- MQTT Publish ----------------
    String baseTopic = "nysd/device/" + stations[stationIndex];

    String voltagePayload = String(voltage, 2);
    if (client.publish((baseTopic + "/voltage").c_str(), voltagePayload.c_str())) {
      Serial.println("✅ Published voltage");
    } else {
      Serial.println("❌ Failed to publish voltage");
    }

    String status = (voltage < 1) ? "ALERT" : "NORMAL";
    if (client.publish((baseTopic + "/status").c_str(), status.c_str())) {
      Serial.println("✅ Published status");
    } else {
      Serial.println("❌ Failed to publish status");
    }
  }
}
