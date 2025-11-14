# outages/mqtt_listener.py
import json
from threading import Thread
import paho.mqtt.client as mqtt
from django.utils import timezone
# IMPORT your models here
from .models import Community  # <-- this was missing
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "nysd/derek/voltage"

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT broker, result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        voltage = float(msg.payload.decode())
        community = Community.objects.first()
        if community:
            community.voltage = voltage
            community.save()
            print(f"Voltage updated: {voltage}")
        else:
            print("❌ No Community found to update")
    except Exception as e:
        print("❌ Error parsing voltage:", e)

def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

def start_mqtt():
    t = Thread(target=mqtt_loop)
    t.daemon = True
    t.start()
    print("🟢 MQTT listener started")
