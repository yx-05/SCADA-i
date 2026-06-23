import paho.mqtt.client as mqtt
import json

# Broker settings matching your Unity script
BROKER = "broker.emqx.io"
PORT = 1883  # Using the standard TCP port for the Python script
TOPICS = [
    ("scada-i-demo/sensors", 0), # Telemetry data
    ("scada-i-demo/status", 0)   # Hardware state feedback
]

# Callback when the script successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Successfully connected to EMQX Broker: {BROKER}")
        client.subscribe(TOPICS)
        print(f"📡 Listening to topics: {[t[0] for t in TOPICS]}")
        print("-" * 50)
    else:
        print(f"❌ Failed to connect. Return code: {rc}")

# Callback when a message arrives from Unity
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    
    print(f"\n📩 [NEW MESSAGE] Topic: {topic}")
    try:
        # Try to format the JSON so it's easy to read
        parsed_json = json.loads(payload)
        print(json.dumps(parsed_json, indent=4))
    except json.JSONDecodeError:
        # If it's somehow not JSON, just print the raw text
        print(payload)

# Initialize the MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER, PORT, 60)

# Keep the script running forever until you press Ctrl+C
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 Disconnected by user.")
    client.disconnect()