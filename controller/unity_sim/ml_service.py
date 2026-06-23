import time
import json
import logging
import pandas as pd
import numpy as np
import joblib
import paho.mqtt.client as mqtt

from GenerateData import GenerateData

# --- CONFIGURATION ---
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
TOPIC_SUBSCRIBE = "scada-i-demo/sensors"
TOPIC_PUBLISH = "scada-i-demo/actions"

# Paths to your trained models
FAN_MODEL_PATH = "models/best_fan_model.joblib"
TEMP_MODEL_PATH = "models/best_temp_model.joblib"

class MLService:
    def __init__(self):
        logging.info("Initializing ML Service...")
        
        self.data_generator = GenerateData()
        
        # Load the Scikit-Learn Models
        try:
            self.fan_model = joblib.load(FAN_MODEL_PATH)
            self.temp_model = joblib.load(TEMP_MODEL_PATH)
            logging.info("Fan and Temperature models loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load models. Ensure they exist in the correct path. Error: {e}")
            self.fan_model = None
            self.temp_model = None

        # Setup MQTT Client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"✅ Connected to MQTT Broker at {MQTT_BROKER}")
            client.subscribe(TOPIC_SUBSCRIBE)
            logging.info(f"📡 Listening for sensor data on: {TOPIC_SUBSCRIBE}")
        else:
            logging.error(f"❌ Failed to connect to broker. Return code: {rc}")

    def _engineer_features(self, df):
        """
        Applies the exact same feature engineering steps used during training.
        """
        df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
        df["is_peak_hour"] = df["hour"].between(12, 17).astype(int)
        
        df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24.0)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24.0)
        df['dayofweek_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
        df['dayofweek_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)
        
        df['temp_diff'] = df['room_temp'] - df['outside_temp']
        
        current_ac_setting = df.get('ac_temp_setting', 23.0) 
        df['set_point_diff'] = df['room_temp'] - current_ac_setting
        
        columns_to_use = [
            'room_temp', 'outside_temp', 'weather_condition', 'is_peak_hour',
            'temp_diff', 'set_point_diff', 'hour_sin', 'hour_cos',
            'dayofweek_sin', 'dayofweek_cos'
        ]
        
        return df[columns_to_use]

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            sensor_data = json.loads(payload)
            
            logging.info(f"📩 Received sensor data: Temp={sensor_data.get('temperature')}C, Occ={sensor_data.get('occupancy')}")

            # Empty room override 
            if sensor_data.get("occupancy", 0) == 0:
                self.publish_action(fan_speed=0, target_temp=0.0)
                logging.info("Room is empty. Action: AC OFF.")
                return

            if self.fan_model and self.temp_model:
                
                # =========================================================
                # INJECTION BLOCK (Fixes GenerateData.py without editing it)
                # =========================================================
                
                # 1. Fix the power usage key mismatch
                if "ac_power_usage" in sensor_data and "power_usage" not in sensor_data:
                    sensor_data["power_usage"] = sensor_data["ac_power_usage"]
                elif "power_usage" not in sensor_data:
                    sensor_data["power_usage"] = 0.0
                    
                # 2. Force weather/time keys to exist so GenerateData skips the API calls
                fallback_defaults = {
                    "outside_temp": 28.0,
                    "outside_humidity": 75.0,
                    "weather_condition": "cloudy",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "hour_of_day": 12,
                    "day_of_week": 0,
                    "day_of_year": 1
                }
                for key, default_val in fallback_defaults.items():
                    if key not in sensor_data:
                        sensor_data[key] = default_val

                # =========================================================

                # Generate base data using the unmodified GenerateData class
                base_df = self.data_generator.generate_column(sensor_data)
                
                # Engineer features
                features_df = self._engineer_features(base_df)
                
                # Run Predictions
                pred_fan_encoded = self.fan_model.predict(features_df)[0]
                pred_temp = self.temp_model.predict(features_df)[0]
                
                # Map fan output
                mapped_fan_speed = self._map_fan_speed(pred_fan_encoded)
                
                # Send command
                self.publish_action(fan_speed=mapped_fan_speed, target_temp=pred_temp)
                logging.info(f"🤖 ML Predicted Action: Fan={mapped_fan_speed} (Raw: {pred_fan_encoded}), Temp={pred_temp:.1f}C")

        except json.JSONDecodeError:
            logging.warning("Received invalid JSON payload.")
        except Exception as e:
            logging.error(f"Error processing message: {e}", exc_info=True)

    def _map_fan_speed(self, encoded_speed):
        """
        Maps the notebook's label encoding back to Unity's FanSpeed Enum.
        """
        mapping = {
            0: 3, # Model High -> Unity High
            1: 1, # Model Low -> Unity Low
            2: 2, # Model Medium -> Unity Medium
            3: 0, # Model Off -> Unity Off
            4: 1  # Model "On" -> Default to Unity Low if generic
        }
        return mapping.get(encoded_speed, 0)

    def publish_action(self, fan_speed: int, target_temp: float):
        action_payload = {
            "fanSpeed": fan_speed,
            "acTempSetting": round(float(target_temp), 1)
        }
        self.client.publish(TOPIC_PUBLISH, json.dumps(action_payload))

    def start(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            logging.info("Shutting down ML Service...")
            self.client.disconnect()
        except Exception as e:
            logging.critical(f"Failed to start MQTT client: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    service = MLService()
    service.start()