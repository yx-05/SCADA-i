import joblib

class ModelLoader:
    def __init__(self, temp_model_path, occupancy_model_path, time_to_cool_model_path):
        print("Loading models...")
        self.models ={
            'temperature': joblib.load(temp_model_path),
            'occupancy': joblib.load(occupancy_model_path),
            'time_to_cool': joblib.load(time_to_cool_model_path)
        }
        print("Models loaded successfully.")
    
    def get(self, model_name):
        return self.models.get(model_name)