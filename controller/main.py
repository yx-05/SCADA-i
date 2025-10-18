# main.py
import time
import logging
import os
import pandas as pd

# To load the model
from ModelLoader import ModelLoader

# To load the orchestrator
from ModelFlow import ModelFlow

# To establish MQTT connection
from MQTTConnection import MQTTConnection

# To store in to SQLite DB
from Database import Database

# To generate the require features for prediction
from GenerateData import GenerateData


# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MQTT
MQTT_BROKER_ADDRESS = "192.168.0.105" # FLAG! need to set to the real address
MQTT_TOPIC = "room/+/device/+/sensor"
# SQLite DB
SQLITE_ADDRESS = os.path.join(BASE_DIR, "Database", "BackendDatabase.db")
# Models path
TEMP_MODEL = os.path.join(BASE_DIR, "models", "best_temp_model.joblib")
OCCUPANCY_MODEL = os.path.join(BASE_DIR, "models", "occupancy_pred.joblib")
TIME_TO_COOL_MODEL = os.path.join(BASE_DIR, "models", "time_to_cool_model.pkl")

class Controller:
    def __init__(self):
        self.mqtt_client = MQTTConnection(MQTT_BROKER_ADDRESS, MQTT_TOPIC)
        self.db = Database(SQLITE_ADDRESS)
        self.generate_data = GenerateData()
        self.models = ModelLoader(TEMP_MODEL, OCCUPANCY_MODEL, TIME_TO_COOL_MODEL)
        self.orchestrator = ModelFlow(self.models)
        self.last_processed_data = None
    
    def run_control_loop(self):
        # FLAG! might need to refactor into smaller functions for Controller.start(), .stop, .run_once
        logging.info("Staring the main controller loop")
        
        # Initialize the connection
        # Retrying mechanism on the first connection
        connected = False
        while not connected:
            try: 
                self.mqtt_client.connect()
                connected = True
            except Exception as e:
                logging.error(f"Failed to connect to MQTT broker on startup: {e}")
                logging.info("Retrying in 5 seconds...")
                time.sleep(5) # Wait for 5 seconds before trying again
        
        # Start the thread to store every single mqtt message in the DB
        self.mqtt_client.start_worker(self.db)
        self.mqtt_client.loop_start()
        
        try:
            while True:
                # Get the latest data
                current_data = self.mqtt_client.get_latest_message()
                
                if current_data and current_data != self.last_processed_data:
                    self.last_processed_data = current_data
                    logging.info(f"New sensor data is received: {current_data}")

                else:
                    logging.info("No new sensor data is received. Will be using previous data.")
                    
                if self.last_processed_data is not None:
                    df = self.generate_data.generate_column(self.last_processed_data)
                    # Get history column
                    try:
                        history_row = self.db.retrieve_latest_sensor_data(3)
                        history_df_list = [self.generate_data.generate_column(r) for r in history_row]
                        history_row = pd.concat(history_df_list, ignore_index=True)
                        df = pd.concat([df, history_row], ignore_index=True)
                        df['timestamp'] = pd.to_datetime(df["timestamp"])
                        df = df.sort_values(by="timestamp", ascending=True, ignore_index=True)
                        logging.info(f"Successfuly retrieve from DB.")
                    except Exception as e:
                        logging.error(f"Error (Main): Error retrieving db values {e}")
                    
                    
                    self.orchestrator.tick(df)
                
                time.sleep(5)
 
        except KeyboardInterrupt:
            logging.info("Shutting down the system...")
            self.mqtt_client.loop_stop()
            
        except Exception as e:
            logging.critical(f"Unexpected error in main loop: {e}", exc_info=True)
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    controller = Controller()
    controller.run_control_loop()