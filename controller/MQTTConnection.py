# A class to establish the connection between the controller and the MQTT Broker

import paho.mqtt.client as mqtt
import json, queue, threading
import logging

# Import Database class to solve the recursive use of cursor error
from Database import Database

class MQTTConnection:
    def __init__(self, broker_address, *TOPIC):
        """
        Initialize connection with MQTT
        Parameters:
            broker_address (str): The MQTT broker IP address
            topic (str): A string contain the topic subscribe 
        """
        self.BROKER_ADDRESS = broker_address
        self.TOPIC = list(TOPIC)
        self.last_sensor_message = None
        self.msg_queue = queue.Queue()
        
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
    def connect(self):
        """Establish connection to MQTT Broker (a blocking call)"""
        try:
            logging.info(f"Connecting to MQTT Broker at {self.BROKER_ADDRESS}")
            self.client.connect(self.BROKER_ADDRESS, 1883, 60)
        except Exception as e:
            logging.error(f"Failed to establlish connection to MQTT Broker: {e}")
            raise
    
    def start_worker(self, db):
        worker_thread = threading.Thread(target=self._worker, args=(db,), daemon=True, name="DBWorker")
        worker_thread.start()
        logging.info("Worker thread started for DB storage")
        
    def get_latest_message(self):
        """Get method to get the latest sensor data"""
        return self.last_sensor_message
    
    def loop_start(self):
        """Start the non-block calling, background thread for listening to the Broker updates"""
        logging.info("Starting MQTT background loop")
        self.client.loop_start()
        
    def loop_stop(self):
        """Stop the background thread"""
        logging.info("Stopping MQTT background loop")
        self.client.loop_stop()
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected with NQTT Broker with code : {rc}")
            if isinstance(self.TOPIC, (list, tuple)):
                for topic in self.TOPIC:
                    client.subscribe(topic)
            else:
                client.subscribe(self.TOPIC)
            logging.info(f"Subscribed to: {self.TOPIC}")
        else:
            logging.error(f"Failed to connect to MQTT Broker with code {rc}")
            
    def _on_message(self, client, userdata, msg):
        part = msg.topic.split('/')
        try:
            payload = json.loads(msg.payload.decode())
            if part[-1] == "sensor":
                device_id = int(part[3])
                
                 # Make a shallow copy
                payload_copy = payload.copy()
                # Inject device_id into the payload
                payload_copy["device_id"] = device_id
                
                logging.info(f"[MQTT > SERVER] -- Message: {payload}")
            
                self.last_sensor_message = payload_copy
            
                # Push into queue for worker
                self.msg_queue.put((device_id, payload))
            elif part[-1] == "response":
                logging.info(f"[APPLICATION > SERVER] -- Message: {payload}")
                device_id = 'app'
                self.msg_queue.put((device_id,payload))
            
        except json.JSONDecodeError:
            logging.warning(f"Received non-JSON message on topic {msg.topic}: {msg.payload.decode()}, not utilizing current state")
            
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            
    def _worker(self, SQLITE_ADDRESS):
        """Background worker that consumes messages from MQTT queue and stores them in the database."""
        db = Database(SQLITE_ADDRESS)
        logging.info("DB worker thread started with its own database connection.")

        try:
            while True:
                device_id, data = self.msg_queue.get()
                try:
                    if device_id != "app":
                        db.store_sensor_data(device_id, data)
                    else:
                        db.store_feedback_data(data)
                except Exception as e:
                    logging.error(f"Error storing data for device {device_id}: {e}")
                finally:
                    self.msg_queue.task_done()

        except Exception as thread_error:
            logging.error(f"Fatal error in DB worker thread: {thread_error}")

        finally:
            db.close()
            logging.info("DB worker thread stopped and database connection closed.")
