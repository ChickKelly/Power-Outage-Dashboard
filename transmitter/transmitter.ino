#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// nRF24L01 pins
RF24 radio(9, 10);
const byte address[6] = "00001";

// Voltage sensor
const int voltagePin = A0;
const float R1 = 30000.0;
const float R2 = 7500.0;
int led1 = 4;
int led2 = 5;
int led3 = 6;
int led4 = 7;

void setup() {
  Serial.begin(9600);
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
  pinMode(led4,OUTPUT);
  if (!radio.begin()) {
    Serial.println("❌ Radio not responding!");
    while (1);
  }
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_1MBPS);
  radio.stopListening();

  Serial.println("Transmitter ready...");
}

void loop() {
  int raw = analogRead(voltagePin);
  float vout = (raw * 5.0) / 1023.0;
  float vin = vout / (R2 / (R1 + R2));  // Actual voltage
  if(vin < 1){
    digitalWrite(led1,LOW);
     digitalWrite(led2,LOW);
      digitalWrite(led3,LOW);
       digitalWrite(led4,LOW);
  }
  else{
     digitalWrite(led1,HIGH);
      digitalWrite(led2,HIGH);
       digitalWrite(led3,HIGH);
        digitalWrite(led4,HIGH);
  }
  Serial.print("Sending voltage: "); Serial.println(vin);

  // Send voltage as float
  radio.write(&vin, sizeof(vin));

  delay(1000);
}
