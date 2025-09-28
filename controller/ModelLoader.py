from API.OccupancyAPI import OccupancyAPI
from API.TempControlAPI import TempControlAPI
from API.TimeToCoolAPI import TimeToCoolAPI

import logging

class ModelLoader:
    def __init__(self, temp_model_path, occupancy_model_path, time_to_cool_model_path):
        logging.info("Loading models...")
        self.models ={
            'occupancy': OccupancyAPI(occupancy_model_path),
            'temperature': TempControlAPI(temp_model_path),
            'time_to_cool': TimeToCoolAPI(time_to_cool_model_path)
        }
        logging.info("Models loaded successfully.")
    
    def get(self, model_name):
        return self.models.get(model_name)