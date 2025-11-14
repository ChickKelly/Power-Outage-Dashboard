#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <nRF24L01.h>
#include <RF24.h>

// WiFi credentials
const char* ssid = "NYSD_PIXEL";
const char* password = "N123456781";

// MQTT broker
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;

// nRF24L01 setup
RF24 radio(9, 10);             // CE, CSN
const byte address[6] = "00001";

// LEDs and buzzer
const int greenLED = 5;
const int redLED = 6;
const int buzzer = 7;

// Wi-Fi and MQTT
WiFiClient wifiClient;
PubSubClient client(wifiClient);

// Timer
unsigned long lastSend = 0;
const unsigned long sendInterval = 1000;

// ====== Setup WiFi ======
void setup_wifi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\n✅ Connected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

// ====== MQTT reconnect ======
void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("VoltageReceiver")) {
      Serial.println("✅ MQTT connected");
    } else {
      Serial.print("❌ MQTT failed (rc=");
      Serial.print(client.state());
      Serial.println("), retrying...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);

  // LEDs/Buzzer
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(buzzer, OUTPUT);
  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);
  digitalWrite(buzzer, LOW);

  // nRF24L01
  if (!radio.begin()) {
    Serial.println("❌ Radio not responding!");
    for (;;);
  }
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_1MBPS);
  radio.startListening();

  // Wi-Fi + MQTT
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  if (radio.available()) {
    float voltage = 0;
    radio.read(&voltage, sizeof(voltage));

    Serial.print("Received voltage: ");
    Serial.println(voltage, 2);

    // LED & buzzer logic
    if (voltage > 0.1) {
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
      digitalWrite(buzzer, LOW);
    } else {
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
      digitalWrite(buzzer, HIGH);
    }

    // Send voltage to MQTT
    char buf[10];
    dtostrf(voltage, 4, 2, buf);
    client.publish("nysd/derek/voltage", buf);
  }

  delay(sendInterval);
}
