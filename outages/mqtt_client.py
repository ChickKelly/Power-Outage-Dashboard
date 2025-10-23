import os, django, json
import paho.mqtt.client as mqtt

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from outages.models import Community

# ---------------- MQTT Config ----------------
MQTT_BROKER = "21981c8197844bccbd5f2c47fec665be.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "hivemq.webclient.1758713241793"
MQTT_PASSWORD = "YOPNa1q5BGH#o.9n:u6W>r"
MQTT_TOPIC = "nysd/status/#"   # listen to all station updates

# ---------------- Handlers ----------------
def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Connected to HiveMQ with result code", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📩 Received on {msg.topic}: {payload}")

        data = json.loads(payload)  # Expect JSON payload
        community_id = data.get("id")
        status = data.get("status")
        voltage = data.get("voltage")

        if not community_id:
            print("⚠️ Missing community ID in payload")
            return

        community = Community.objects.get(id=community_id)
        community.power_status = (status.upper() == "OK")
        community.save()

        print(f"⚡ Community {community.name} updated → "
              f"Status: {status}, Voltage: {voltage}")

    except Exception as e:
        print("❌ Error processing message:", e)

# ---------------- MQTT Client ----------------
client = mqtt.Client(client_id="django-listener", protocol=mqtt.MQTTv311, transport="tcp")
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()  # Use TLS
client.tls_insecure_set(True)  # Ignore cert validation for dev

client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
