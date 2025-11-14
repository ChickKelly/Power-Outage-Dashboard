import threading
import time
import paho.mqtt.client as mqtt
from django.utils import timezone
import django
import os

# Setup Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "power_outage_alert.settings")
django.setup()

from .models import VoltageReading, Community  # adjust if your model is in another file

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "nysd/derek/voltage"

# Called when connected to broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

# Called when a message is received
def on_message(client, userdata, msg):
    try:
        value = float(msg.payload.decode())  # convert payload to float
        print(f"Received voltage: {value}")
        
        # Example: assign to a default community (change as needed)
        community = Community.objects.first()
        if community:
            VoltageReading.objects.create(
                community=community,
                value=value,
                timestamp=timezone.now()
            )
    except Exception as e:
        print("Error saving voltage:", e)

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# Run in separate thread if needed
threading.Thread(target=start_mqtt, daemon=True).start()
