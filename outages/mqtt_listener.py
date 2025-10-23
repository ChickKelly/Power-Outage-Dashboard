# outages/mqtt_listener.py
from django.utils import timezone

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📩 Received on {msg.topic}: {payload}")

        data = json.loads(payload)  # Expect {"id": 1, "status": "OK", "voltage": 220.5}
        community_id = data.get("id")
        status = data.get("status")
        voltage = data.get("voltage")

        if not community_id:
            print("⚠️ Missing community ID in payload")
            return

        community = Community.objects.get(id=community_id)
        community.power_status = (status.upper() == "OK")
        community.voltage = voltage if voltage is not None else 0.0
        community.last_update = timezone.now()
        community.save()

        print(f"⚡ Updated {community.name} → Status={status}, Voltage={voltage}")

    except Exception as e:
        print("❌ Error processing message:", e)
