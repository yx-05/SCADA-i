import paho.mqtt.client as mqtt
import sqlite3
import json
import time

DB_PATH = "INSERT DATABASE'S PATH HERE"

def set_sensor_data(device_id, data):
    conn = sqlite3.connection(DB_PATH)
    cursor = conn.cursor()

    cursor.execute
    ("""
        INSERT INTO sensor_data (device_id, timestamp, temperature, humidity, occupancy, power_usage)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
            device_id,
            str(time.time()), 
            data.get("temperature"),
            data.get("humidity"),
            data.get("occupancy"),
            data.get("power_usage")
        )
    )

    cursor.execute
    ("""
        INSERT INTO realtime_state (device_id, last_update, temperature, humidity, occupancy, power_usage)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(device_id) DO UPDATE SET
            last_update=excluded.last_update,
            temperature=excluded.temperature,
            humidity=excluded.humidity,
            occupancy=excluded.occupancy,
            power_usage=excluded.power_usage
    """, (
            device_id,
            str(time.time()),
            data.get("temperature"),
            data.get("humidity"),
            data.get("occupancy"),
            data.get("power_usage")
        )
    )

    conn.commit()
    conn.close()

def on_connect(client, userdata, flags, rc):
    print("Connected with NQTT Broker with code : " + rc)
    client.subscribe("room/+/device/+/sensor")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[ESP32 > SERVER] -- {payload}")

        part = msg.topic.split('/')
        device_id = int(part[3])
        
        set_sensor_data(device_id, payload)
    
    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message 

client.connect("INSERT MQTT BROKER'S IP HERE", 1883, 60)
client.loop_forever()