# import time
# import json
# import random
# import paho.mqtt.client as mqtt

# # ----------- MQTT Configuration -----------
# BROKER = "127.0.0.1"
# PORT = 1883
# TOPIC_T1 = "room/1/device/1/sensor"
# TOPIC_T2 = "room/1/device/2/sensor"

# # ----------- Timing (seconds) -----------
# PUBLISH_INTERVAL = 3       # Both devices send together every 3s
# PIR_INTERVAL = 30
# HOG_THRESHOLD = 20

# # ----------- State Variables -----------
# occ_t1 = 0
# occ_t2 = 0
# hog_t1 = 0
# us_detect_count_t1 = 0

# last_pir_check = time.time()
# last_publish_check = time.time()

# # ----------- MQTT Client Setup -----------
# client = mqtt.Client()

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("✅ MQTT Connected")
#     else:
#         print(f"❌ Failed to connect, return code {rc}")

# client.on_connect = on_connect
# client.connect(BROKER, PORT, 60)
# client.loop_start()

# # ----------- Simulation Helper Functions -----------
# def simulate_pir():
#     """Randomly simulate PIR trigger (motion detection)."""
#     return random.choice([0, 1])

# def simulate_ultrasonic_t1():
#     """Simulate ultrasonic readings for Table 1 (top & bottom)."""
#     d_top = random.randint(20, 70)
#     d_bottom = random.randint(10, 60)
#     return d_top, d_bottom

# def simulate_ultrasonic_t2():
#     """Simulate ultrasonic reading for Table 2."""
#     return random.randint(10, 60)

# # ----------- Main Loop -----------
# try:
#     while True:
#         now = time.time()

#         # --- PIR Check ---
#         if now - last_pir_check > PIR_INTERVAL:
#             last_pir_check = now
#             pir_val = simulate_pir()
#             if pir_val == 1:
#                 occ_t1 = 1
#                 hog_t1 = 0
#                 us_detect_count_t1 = 0
#             else:
#                 occ_t1 = 0

#         # --- Publish both devices at the same time ---
#         if now - last_publish_check > PUBLISH_INTERVAL:
#             last_publish_check = now

#             # --- Ultrasonic T1 ---
#             d_top, d_bottom = simulate_ultrasonic_t1()
#             detect_t1 = (0 < d_top < 50) or (0 < d_bottom < 40)

#             if occ_t1 == 0 and detect_t1:
#                 us_detect_count_t1 += 1
#                 if us_detect_count_t1 >= HOG_THRESHOLD:
#                     hog_t1 = 1
#             elif occ_t1 == 1:
#                 us_detect_count_t1 = 0

#             payload_t1 = {
#                 "temperature": 25,
#                 "humidity": 25,
#                 "occupancy": occ_t1,
#                 "power_usage": 25,
#                 "seat_hogged": hog_t1
#             }
#             client.publish(TOPIC_T1, json.dumps(payload_t1))
#             print(f"[T1] Published occ={occ_t1}, hog={hog_t1}, count={us_detect_count_t1}, top={d_top}cm, bottom={d_bottom}cm")

#             # --- Ultrasonic T2 ---
#             d_bottom_t2 = simulate_ultrasonic_t2()
#             occ_t2 = 1 if (0 < d_bottom_t2 < 40) else 0

#             payload_t2 = {
#                 "temperature": 26,
#                 "humidity": 26,
#                 "occupancy": occ_t2,
#                 "power_usage": 26,
#                 "seat_hogged": hog_t1
#             }
#             client.publish(TOPIC_T2, json.dumps(payload_t2))
#             print(f"[T2] Published occ={occ_t2}, bottom={d_bottom_t2}cm")

#         time.sleep(0.1)

# except KeyboardInterrupt:
#     print("\n🛑 Simulation stopped.")
#     client.loop_stop()
#     client.disconnect()

import time
import json
import random
import paho.mqtt.client as mqtt

# ----------- MQTT Configuration -----------
BROKER = "127.0.0.1"
PORT = 1883
TOPIC_T1 = "room/1/device/1/sensor"
TOPIC_T2 = "room/1/device/2/sensor"
TOPIC_RESPONSE = "room/1/manual_override/response"

# ----------- Timing (seconds) -----------
PUBLISH_INTERVAL = 3        # Both devices send together every 3s
PIR_INTERVAL = 30
HOG_THRESHOLD = 20
RESPONSE_INTERVAL = 15      # Every 15 seconds, publish manual override

# ----------- State Variables -----------
occ_t1 = 0
occ_t2 = 0
hog_t1 = 0
us_detect_count_t1 = 0

last_pir_check = time.time()
last_publish_check = time.time()
last_response_check = time.time()

# ----------- MQTT Client Setup -----------
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT Connected")
    else:
        print(f"❌ Failed to connect, return code {rc}")

client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

# ----------- Simulation Helper Functions -----------
def simulate_pir():
    """Randomly simulate PIR trigger (motion detection)."""
    return random.choice([0, 1])

def simulate_ultrasonic_t1():
    """Simulate ultrasonic readings for Table 1 (top & bottom)."""
    d_top = random.randint(20, 70)
    d_bottom = random.randint(10, 60)
    return d_top, d_bottom

def simulate_ultrasonic_t2():
    """Simulate ultrasonic reading for Table 2."""
    return random.randint(10, 60)

def simulate_manual_override():
    """Simulate a user-submitted manual override request."""
    selectedHardware = random.choice(["Fan", "Light", "Projector", "AC"])
    name = random.choice(["Alice", "Bob", "Charlie", "Diana"])
    email = f"{name.lower()}@example.com"
    change = random.choice(["Increase brightness", "Turn off AC", "Reduce temperature"])
    reason = random.choice(["Too cold", "Too hot", "Too noisy", "Energy saving"])
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "hardware": selectedHardware,
        "name": name,
        "email": email,
        "change": change,
        "reason": reason,
        "timestamp": timestamp,
    }

# ----------- Main Loop -----------
try:
    while True:
        now = time.time()

        # --- PIR Check ---
        if now - last_pir_check > PIR_INTERVAL:
            last_pir_check = now
            pir_val = simulate_pir()
            if pir_val == 1:
                occ_t1 = 1
                hog_t1 = 0
                us_detect_count_t1 = 0
            else:
                occ_t1 = 0

        # --- Publish sensor data ---
        if now - last_publish_check > PUBLISH_INTERVAL:
            last_publish_check = now

            # --- Ultrasonic T1 ---
            d_top, d_bottom = simulate_ultrasonic_t1()
            detect_t1 = (0 < d_top < 50) or (0 < d_bottom < 40)

            if occ_t1 == 0 and detect_t1:
                us_detect_count_t1 += 1
                if us_detect_count_t1 >= HOG_THRESHOLD:
                    hog_t1 = 1
            elif occ_t1 == 1:
                us_detect_count_t1 = 0

            payload_t1 = {
                "temperature": 25,
                "humidity": 25,
                "occupancy": occ_t1,
                "power_usage": 25,
                "seat_hogged": hog_t1
            }
            client.publish(TOPIC_T1, json.dumps(payload_t1))
            print(f"[T1] Published occ={occ_t1}, hog={hog_t1}, count={us_detect_count_t1}, top={d_top}cm, bottom={d_bottom}cm")

            # --- Ultrasonic T2 ---
            d_bottom_t2 = simulate_ultrasonic_t2()
            occ_t2 = 1 if (0 < d_bottom_t2 < 40) else 0

            payload_t2 = {
                "temperature": 26,
                "humidity": 26,
                "occupancy": occ_t2,
                "power_usage": 26,
                "seat_hogged": hog_t1
            }
            client.publish(TOPIC_T2, json.dumps(payload_t2))
            print(f"[T2] Published occ={occ_t2}, bottom={d_bottom_t2}cm")

        # --- Publish Manual Override Response ---
        if now - last_response_check > RESPONSE_INTERVAL:
            last_response_check = now
            final_request = simulate_manual_override()
            client.publish(TOPIC_RESPONSE, json.dumps(final_request))
            print(f"[APP] Published manual override: {final_request}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Simulation stopped.")
    client.loop_stop()
    client.disconnect()
