import time
from datetime import datetime, timedelta
from ModelLoader import ModelLoader
from SystemState import SystemState

class MainController:
    def __init__(self, models: ModelLoader):
        self.model = models
        self.state = SystemState.IDLE
        self.predicted_occupancy_time = None
        self.pre_cool_start_time = None
        print(f"Controller Initilized. Starting state: {self.state.name}")
    
    def tick(self, current_sensor_data):
        """
        Process that run on every tick
        Parameters:
            current_sensor_data: columns of recent sensor data
        """
        print(f"\nTick at {datetime.now()} | Current State: {self.state.name}")
        
        # State Transition Logic
        if self.state == SystemState.OCCUPIED:
            # If room becomes empty, transition to saving mode
            if not current_sensor_data['occupied']:
                self._set_to_IDLE(current_sensor_data)

        elif self.state == SystemState.IDLE:
            # If room becomes occupied unexpectedly, transition to cooling
            if current_sensor_data['occupied']:
                self._set_to_OCCUPIED()
            # If it's time to start pre-cooling
            elif datetime.now() >= self.pre_cool_start_time:
                self._set_to_PRE_COOLING()
            # If we missed the occupancy window
            # elif datetime.now() > self.predicted_occupancy_time + timedelta(minutes=15): # 15 min grace period
            #     self._set_to_ERROR("Occupancy time passed.")

        elif self.state == SystemState.PRE_COOLING:
            # # If room becomes occupied during pre-cool, transition to normal cooling
            # if current_sensor_data['occupied']:
            #     self._transition_to_cooling_occupied()
            # If target temperature is reached
            if current_sensor_data['temperature'] <= 23:
                print("Target pre-cool temperature reached. Waiting for occupant.")
        
        # Perform action
        self._perform_state_action(current_sensor_data)
        
    def _perform_state_action(self, sensor_data):
        if self.state == SystemState.OCCUPIED:
            temp_model = self.model.get('temperature')
            actions = temp_model.predict(sensor_data) 
            print(f"State: OCCUPIED, Action: temperature control: {actions}")
        
        elif self.state == SystemState.IDLE:
            print(f"State: IDLE, Action: Turn off air conditioner. Next pre-cooling {self.pre_cool_start_time}")
            
        elif self.state == SystemState.PRE_COOLING:
            print("State: PRE_COOLING, Action: temperature set to 22, fan power high.")
        
        elif self.state == SystemState.ERROR:
            print("Action: System in error state. Requires manual reset or new prediction.")
    
    def _set_to_IDLE(self):
        pass
    
    def _set_to_OCCUPIED(self):
        pass

    def _set_to_PRE_COOLING(self):
        pass

    def _set_to_ERROR(self):
        pass
