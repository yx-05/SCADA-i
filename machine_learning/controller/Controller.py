from datetime import datetime, timedelta
from ModelLoader import ModelLoader
from SystemState import SystemState

class Controller:
    def __init__(self, models: ModelLoader):
        self.model = models
        self.state = SystemState.IDLE
        self.pre_cool_start_time = None
        
        self.OCCUPANCY_PROB_THRES = 0.5
        self.last_occ_pred_time = None
        self.predicted_arrival_deadline = None
        self.PREDICTION_INTERVAL = timedelta(minutes=50) # How often to re-predict in IDLE state.
        self.TARGET_TEMP = 23.0
        print(f"Controller Initilized. Starting state: {self.state.name}")
    
    def tick(self, current_sensor_data):
        """
        Process that run on every tick
        Parameters:
            current_sensor_data: columns of recent sensor data
        """
        print(f"\nTick at {datetime.now()} | Current State: {self.state.name}")
        
        
        # Always change to OCCUPIED first if occupied
        if current_sensor_data['occupied']:
            if self.state != SystemState.OCCUPIED:
                # log the suprise occupancy
                print("Surprise occupancy detected (False Negative). Logging the event.")
                self._set_to_OCCUPIED()
        
        # State Transition Logic
        if self.state == SystemState.OCCUPIED:
            # If room becomes empty, transition to saving mode
            if not current_sensor_data['occupied']:
                self._set_to_IDLE(current_sensor_data)

        elif self.state == SystemState.IDLE:
            # If it's time to start pre-cooling
            time_since_last_pred = (datetime.now() - self.last_occ_pred_time) if self.last_occ_pred_time else self.PREDICTION_INTERVAL
            
            if time_since_last_pred >= self.PREDICTION_INTERVAL:
                print("Prediction interval elapsed. Re-evaluating pre-cool schedule.")
                # Re-run the scheduling logic.
                self._schedule_next_precool(current_sensor_data)

            if self.pre_cool_start_time:
                print(f"  Next pre-cooling scheduled for: {self.pre_cool_start_time}")
            else:
                print("  No pre-cooling is currently scheduled.")
            
            if self.pre_cool_start_time and datetime.now() >= self.pre_cool_start_time:
                self._set_to_PRE_COOLING()

        elif self.state == SystemState.PRE_COOLING:
            if current_sensor_data['temperature'] <= 23:
                print("Target pre-cool temperature reached. Waiting for occupant.")
                self._set_to_PRE_COOLING_FINISH()
        
        elif self.state == SystemState.PRE_COOLING_FINISH:
            # The room is occupied
            if current_sensor_data['occupied']:
                self._set_to_OCCUPIED()
                
            # Set 15 minutes grace period before we flag the error
            elif self.predicted_arrival_deadline and datetime.now() > self.predicted_arrival_deadline + timedelta(minutes=15):
                # Flag the error
                # self._set_to_ERROR("Predicted") # FLAG this
                print("Log the error of prediction")
                self._set_to_IDLE(current_sensor_data)
        
        # Perform action for each tick
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
            
        elif self.state == SystemState.PRE_COOLING_FINISH:
            print("State: PRE_COOLING_FINISH, Action: Turn off air conditioner, grace period of 15 minutes waiting for occupancy.")
        
        # elif self.state == SystemState.ERROR:
        #     print("Action: System in error state. Requires manual reset or new prediction.")
    
    def _set_to_IDLE(self, sensor_data):
        print("Setting to IDLE")
        self.state = SystemState.IDLE
        
        # Calculate when to start pre-cooling
        self._schedule_next_precool(sensor_data)
        
        # print(f"  Will start pre-cooling at: {self.pre_cool_start_time}")
    
    def _set_to_OCCUPIED(self):
        print("Setting to OCCUPIED")
        self.state = SystemState.OCCUPIED
        
        self.pre_cool_start_time = None
        self.predicted_arrival_deadline = None
        self.last_occ_pred_time = None

    def _set_to_PRE_COOLING(self):
        print("Setting to PRE_COOLING")
        self.state = SystemState.PRE_COOLING
        
    def _set_to_PRE_COOLING_FINISH(self):
        print("Setting to PRE_COOLING_FINISH")
        self.state = SystemState.PRE_COOLING_FINISH

    # def _set_to_ERROR(self):
    #     print("Logging occupancy prediction error")
    #     self.state = SystemState.ERROR
    
    def _schedule_next_precool(self, sensor_data):
        
        print("Scheduling next pre-cool time")
        
        self.last_occ_pred_time = datetime.now()
        
        # Run occupancy model
        occ_model = self.model.get("occupancy")
        next_hr_occ_prob = occ_model.predict(sensor_data)
        
        print(f"Predicted occupancy probability for next hour: {next_hr_occ_prob:.2f}")
        
        if next_hr_occ_prob > self.OCCUPANCY_PROB_THRES:
            # Record down the predicted time for occupancy
            self.predicted_arrival_deadline = self.last_occ_pred_time + timedelta(hours=1)
            
            # Run time-to-cool model
            time_to_cool_model = self.model.get('time_to_cool')
            cool_duration = time_to_cool_model.predict(sensor_data)
            
            # Ensure that it is a timedelta for calculation
            if not isinstance(cool_duration, timedelta):
                cool_duration = timedelta(minutes=cool_duration)
            
            buffer = timedelta(minutes=1) 
            target_time = self.last_occ_pred_time + timedelta(hours=1)
            self.pre_cool_start_time = max((target_time - cool_duration), datetime.now() + buffer)
            
            print(f"High probability detected. Estimated cooling time: {cool_duration}.")
            
        else:
            self.pre_cool_start_time = None
            self.predicted_arrival_deadline = None
            print("Low probability detected. No pre-cooling scheduled.")