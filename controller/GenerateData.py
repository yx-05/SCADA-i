import pandas as pd
import numpy as np
from datetime import datetime
import requests
import logging
import json

class GenerateData:
    # def __init__(self, sensor_data):
    #     self.generate_column(sensor_data)
    
    def generate_column(self, sensor_data):
        
        # Check if time features are provided in payload, otherwise generate them
        if all(key in sensor_data for key in ["timestamp", "hour_of_day", "day_of_week", "day_of_year"]):
            timestamp = sensor_data.get("timestamp")
            hour_of_day = sensor_data.get("hour_of_day")
            day_of_week = sensor_data.get("day_of_week")
            day_of_year = sensor_data.get("day_of_year")
            logging.info("Using time features from payload")
        else:
            timestamp, hour_of_day, day_of_week, day_of_year = self._generate_time_features()
            logging.info("Generating time features locally")
        
        # Check if outside features are provided in payload, otherwise fetch from API
        if all(key in sensor_data for key in ["outside_temp", "outside_humidity", "weather_condition"]):
            outside_temp = sensor_data.get("outside_temp")
            outside_humidity = sensor_data.get("outside_humidity")
            weather_condition = sensor_data.get("weather_condition")
            logging.info("Using outside features from payload")
        else:
            outside_temp, outside_humidity, weather_condition = self._generate_outside_features()
            logging.info("Fetching outside features from API")
        
        # Get occupancy features
        # FLAG! need to confirm on how occupancy would be counted. For now assume will get grom MQTT Broker
        occupancy_count = sensor_data.get("occupancy")
        is_occupied = int(occupancy_count > 0)
        
        room_temp = sensor_data.get("temperature")
        # These feature will need to add during the model fixing, but for now just ignore them cuz the model doesnt recognise them
        # room_humidity = sensor_data.get("humidity")
        
        # Air cond setting features
        # FLAG! in real world we wont be able to get these data, so need to retrain the model. But for know just use it
        ac_temp_setting = 23
        fan_speed = "high"
        ac_control_reason = "ACTION: Gentle cooling (slightly warm)"
        
        # Power usage features
        # FLAG! in real world we wont be able to get these data, so need to retrain the model. But for know just use it
        power_kw = sensor_data.get("power_usage")
        
        data = {
            "timestamp": [timestamp],
            "hour_of_day": [hour_of_day],
            "day_of_week": [day_of_week],
            "day_of_year": [day_of_year],
            "outside_temp": [outside_temp],
            "outside_humidity": [outside_humidity],
            "weather_condition": [weather_condition],
            "occupancy_count": [occupancy_count],
            "is_occupied": [is_occupied],
            "room_temp": [room_temp],
            # "room_humidity": [room_humidity],  # optional
            "ac_temp_setting": [ac_temp_setting],
            "fan_speed": [fan_speed],
            "ac_control_reason": [ac_control_reason],
            "power_kw": [power_kw]
        }

        # Convert in to df
        df = pd.DataFrame(data)
        
        return df
        
    def _generate_time_features(self):
        now = datetime.now()
        # Format as "yy-mm-dd h:m:s"
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        hour_of_day = now.hour          # 0–23
        day_of_week = now.weekday()
        day_of_year = now.timetuple().tm_yday   # 1–366
        return timestamp, hour_of_day, day_of_week, day_of_year

    def _generate_outside_features(self):
        API_URL = "https://api.open-meteo.com/v1/forecast?latitude=2.93527&longitude=101.69112&current=temperature_2m,relative_humidity_2m,weathercode"
        
        # Default values
        default_temperature = 25
        default_humidity = 50
        default_weather = "cloudy"
        
        # Get outside features from external api sources
        try:
            response = requests.get(API_URL, timeout=5)
            
            # Check http status code
            if response.status_code != 200:
                logging.error(f"Error (GenerateData): API returned {response.status_code}")
                return default_temperature, default_humidity, default_weather
            
            data = response.json()
            
            # Extract the data, return None if empty, will be handled in preprocessing
            current = data.get("current", {})
            temperature = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            weather_code = self._translate_weather_code(current.get("weathercode"))
            
            return temperature, humidity, weather_code
        
        except requests.exceptions.ConnectionError:
            logging.error("Error (GenerateData): Unable to connect to API")
        except requests.exceptions.Timeout:
            logging.error("Error (GenerateData): Request timed out")
        except json.JSONDecodeError:
            logging.error("Error (GenerateData): Failed to parse JSON")
        except Exception as e:
            logging.error(f"Error (GenerateData): Unexpected error {e}")

        return default_temperature, default_humidity, default_weather
    
    def _translate_weather_code(self, code: int) -> str:
        """
        Translate Open-Meteo weather codes into simplified categories:
        - sunny
        - cloudy
        - rainy
        """
        if code == None:
            # "cloudy" as default
            return "cloudy"
        
        sunny_codes = {0, 1}                    # Clear / mainly clear
        cloudy_codes = {2, 3, 45, 48}           # Cloudy / fog
        rainy_codes = {51, 53, 55, 56, 57,      # Drizzle
                    61, 63, 65, 66, 67,         # Rain
                    80, 81, 82,                 # Rain showers
                    95, 96, 99}                 # Thunderstorms

        if code in sunny_codes:
            return "sunny"
        elif code in cloudy_codes:
            return "cloudy"
        elif code in rainy_codes:
            return "rainy"
        else:
            # "cloudy" as default
            return "cloudy"
        
# Testing
def test_model_preprocess():
    # Sample sensor data
    sample_data = {
        "temperature": 25.5,
        "occupancy": 3,
        "power_usage": 1.2
    }

    # Initialize preprocessing class
    preprocess = GenerateData(sample_data)

    # Generate dataframe
    df = preprocess.generate_column(sample_data)

    print("Generated DataFrame:")
    print(df)

    # Basic assertions
    assert isinstance(df, pd.DataFrame), "Output is not a DataFrame"
    assert "timestamp" in df.columns, "Missing timestamp column"
    assert df["occupancy_count"].iloc[0] == sample_data["occupancy"], "Occupancy value mismatch"
    assert df["room_temp"].iloc[0] == sample_data["temperature"], "Temperature value mismatch"
    assert df["power_kw"].iloc[0] == sample_data["power_usage"], "Power usage value mismatch"

    # Check weather feature (it should return a string, even if API fails)
    assert isinstance(df["weather_condition"].iloc[0], str), "Weather condition should be string"

    print("All tests passed!")

if __name__ == "__main__":
    test_model_preprocess()