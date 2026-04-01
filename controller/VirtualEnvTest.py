import paho.mqtt.client as mqtt
import json

# --- Configuration ---
BROKER = "127.0.0.1"
PORT = 1883
TOPIC_SUB = "simulation/sensors"
TOPIC_PUB = "simulation/actions"

def predict_hvac_action(sensor_data):
    """
    Smart dummy-rule system to prove the connection works.
    Only predicts Fan Speed and AC Temp Setting.
    """
    room_temp = sensor_data.get("roomTemp", 26.0)
    outside_temp = sensor_data.get("outsideTemp", 28.0)
    occupancy = sensor_data.get("occupancyCount", 0)

    # Default action: OFF
    action = {
        "fanSpeed": 0,
        "acTempSetting": 0.0
    }

    if occupancy > 0:
        # People are in the room, keep them cool!
        if room_temp > 24.0:
            action["fanSpeed"] = 3 # High
            action["acTempSetting"] = 20.0
        elif room_temp > 22.0:
            action["fanSpeed"] = 2 # Medium
            action["acTempSetting"] = 22.0
        else:
            action["fanSpeed"] = 1 # Low
            action["acTempSetting"] = 23.0
    else:
        # Predictive Pre-cooling check
        if outside_temp >= 30.0 and room_temp > 25.0:
            print("🧠 ML Prediction: Hot day detected! Activating Predictive Pre-cooling.")
            action["fanSpeed"] = 1 # Low
            action["acTempSetting"] = 24.0
        else:
            # Normal empty room behavior
            action["fanSpeed"] = 0
            action["acTempSetting"] = 0.0

    return action

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connected to MQTT Broker at {BROKER}")
        client.subscribe(TOPIC_SUB)
        print(f"📡 Listening for Unity data on '{TOPIC_SUB}'...\n")
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        # 1. Receive and parse the JSON from Unity
        payload = msg.payload.decode('utf-8')
        sensor_data = json.loads(payload)
        
        print(f"📥 Received Sensor Data: {sensor_data}")

        # 2. Feed data to the "ML Model"
        action = predict_hvac_action(sensor_data)

        # 3. Send the decision back to Unity
        action_json = json.dumps(action)
        client.publish(TOPIC_PUB, action_json)
        
        print(f"📤 Sent ML Action: {action_json}\n")

    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Disconnected by user.")
        client.disconnect()