# main.py
import time
import random # For our sensor simulator
from ModelLoader import ModelLoader
from Controller import Controller

def get_simulated_sensor_data():
    """A dummy function to simulate reading from a sensor."""
    # In a real system, this would read from your database or a live feed.
    return {
        'temperature': round(random.uniform(22.0, 28.0), 1),
        'humidity': round(random.uniform(40.0, 75.0), 1),
        'occupied': random.choice([True, False]) # Randomly simulate occupancy
    }

if __name__ == "__main__":
    # 1. Initialize
    # Replace with the actual paths to your saved model files
    models = ModelLoader(
        temp_model_path='temp_model.joblib',
        occupancy_model_path='occupancy_model.joblib',
        time_to_cool_path='time_to_cool.joblib'
    )
    
    controller = Controller(models)
    
    # 2. Run the main control loop
    try:
        while True:
            # Get the latest data from the environment
            sensor_data = get_simulated_sensor_data()
            
            # Execute one cycle of the controller's logic
            controller.tick(sensor_data)
            
            # Wait for a short period before the next cycle
            time.sleep(10) # Check every 10 seconds

    except KeyboardInterrupt:
        print("\nShutting down controller.")