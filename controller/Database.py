# Database.py
# Database utility class
# Define the connection to db and collect the function to retreive or store data in the db

import sqlite3
from datetime import datetime
import logging

class Database():
    def __init__(self, DB_PATH):
        """Initialize the connection with sqlite"""
        self.DB_PATH = DB_PATH
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to SQLite database and create a cursor."""
        try:
            self.conn = sqlite3.connect(self.DB_PATH, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"Connected to {self.DB_PATH} successfully")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    
    def store_sensor_data(self, device_id, data):
        """Storing the MQTT JSON payload sensor data into DB"""
        try:
            self.cursor.execute("""
                INSERT INTO sensor_data (device_id, timestamp, temperature, humidity, occupancy, power_usage, seat_hogged)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                    device_id,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    float(data.get("temperature", 0.0)),
                    float(data.get("humidity", 0.0)),        
                    int(data.get("occupancy", 0)),             
                    float(data.get("power_usage", 0.0)),
                    int(data.get("seat_hogged", 0))
            ))

            self.cursor.execute("""
                INSERT INTO realtime_state (device_id, last_update, temperature, humidity, occupancy, power_usage, seat_hogged)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(device_id) DO UPDATE SET
                    last_update=excluded.last_update,
                    temperature=excluded.temperature,
                    humidity=excluded.humidity,
                    occupancy=excluded.occupancy,
                    power_usage=excluded.power_usage,
                    seat_hogged=excluded.seat_hogged
            """, (
                    device_id,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    float(data.get("temperature", 0.0)),
                    float(data.get("humidity", 0.0)),        
                    int(data.get("occupancy", 0)),             
                    float(data.get("power_usage", 0.0)),
                    int(data.get("seat_hogged", 0))
            ))
            
            self.conn.commit()
            logging.info("Sensor data stored successfully.")
            
        except sqlite3.Error as e:
            logging.error(f"Error storing sensor data: {e}")
            
    def store_feedback_data(self, data):
        """Store user feedback form data into the feedback_requests table"""
        try:
            self.cursor.execute("""
                INSERT INTO feedback_requests (hardware, name, email, change_req, reason, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get("hardware", "Unknown"),             # Hardware/device name
                data.get("name", "Anonymous"),               # User's name
                data.get("email", "N/A"),                    # User's email
                data.get("change", "No change specified"),   # Requested change
                data.get("reason", "No reason provided"),    # Reason for request
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Current timestamp
            ))

            self.conn.commit()
            logging.info("Feedback data stored successfully.")
        except Exception as e:
            logging.error(f"Error storing feedback data: {e}")

    
    def retrieve_latest_sensor_data(self, row):
        """Retreive latest history data as JSON from table sensor_data"""
        try:
            self.cursor.execute(
                """
                SELECT *
                FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT ?
                """, (row,)
            )
            rows = self.cursor.fetchall()
            result = [dict(row) for row in rows]
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []
        
    def get_all_current_occupancy(self):
        """Return {device_id: occupancy_value} for all devices from realtime_state"""
        try:
            self.cursor.execute("""
                SELECT device_id, occupancy FROM realtime_state
            """)
            rows = self.cursor.fetchall()
            return {row["device_id"]: row["occupancy"] for row in rows}
        except Exception as e:
            logging.error(f"Error retrieving occupancy map: {e}")
            return {}
        
    def close(self):
        if self.conn:
            self.conn.close()
        