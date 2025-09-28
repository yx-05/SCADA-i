import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# MQTT broker details
BROKER = "192.168.0.9"
PORT = 1883
TOPIC = "room/room1/device/1/sensor"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

def publish_data(phase, room_temp, outside_temp, occupancy, power_usage):
    data = {
        "temperature": room_temp,
        "outside_temp": outside_temp,
        "outside_humidity": 70.0,
        "weather_condition": "sunny",
        "ac_temp_setting": 24.0,
        "power_usage": power_usage,
        "occupancy": occupancy,
        "is_occupied": 1 if occupancy > 0 else 0,
        "timestamp": str(datetime.now()),
        "phase": phase  # just for debugging
    }
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    print(f"[{phase}] Published: {payload}")

try:
    # ---- Idle Phase ----
    for _ in range(5):
        publish_data("IDLE", room_temp=29.0, outside_temp=33.0, occupancy=0, power_usage=0)
        time.sleep(3)

    # ---- Pre-Cool Phase ----
    for step in range(5):
        publish_data("PRE-COOL", room_temp=28.5 - step*0.2, outside_temp=33.0, occupancy=0, power_usage=200)
        time.sleep(3)

    # ---- Occupied Phase ----
    for step in range(5):
        publish_data("OCCUPIED", room_temp=27.0 - step*0.3, outside_temp=33.0, occupancy=2, power_usage=600)
        time.sleep(3)

    # ---- Back to Idle Phase ----
    for _ in range(5):
        publish_data("IDLE", room_temp=28.0, outside_temp=33.0, occupancy=0, power_usage=0)
        time.sleep(3)

except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
