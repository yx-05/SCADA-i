import pandas as pd
import numpy as np
import datetime

# --- CONFIGURATION PARAMETERS (Tweak these to change the simulation) ---

# Time settings
DATA_START_DATE = "2023-01-01"
DATA_END_DATE = "2023-12-31"
TIME_FREQUENCY_MIN = 5  # Generate a data point every 5 minutes

# Room thermal properties
HEAT_TRANSFER_COEFFICIENT = 0.05  # How quickly the room temp moves towards the outside temp
HEAT_FROM_OCCUPANT = 0.1         # Heat generated per person per 5 min (°C)
AC_COOLING_POWER = 0.5           # Cooling power of the AC per 5 min (°C)

# Occupancy patterns (simulating a typical office)
WEEKDAY_OCCUPANCY_PROB = {
    # Hour: (Probability of being occupied, Max occupants)
    **{h: (0.0, 0) for h in range(0, 8)},      # Night
    8: (0.3, 3), 9: (0.8, 5), 10: (0.9, 5), 11: (0.9, 5), # Morning
    12: (0.5, 5),                             # Lunch dip
    13: (0.9, 5), 14: (0.9, 5), 15: (0.9, 5), 16: (0.8, 5), # Afternoon
    17: (0.4, 3), 18: (0.2, 2),               # Evening
    **{h: (0.0, 0) for h in range(19, 24)},   # Night
}
WEEKEND_OCCUPANCY_PROB = 0.05 # Small chance of occupancy on weekends

# Thermostat simulation logic
COMFORT_TEMP_MAX = 25.0  # AC turns ON if occupied and temp is above this
COMFORT_TEMP_MIN = 23.0  # AC turns OFF if temp is below this

# --- DATA GENERATION FUNCTIONS ---

def generate_base_timeline(start_date, end_date, freq_min):
    """Creates the main DataFrame with timestamps."""
    print(f"Generating timeline from {start_date} to {end_date}...")
    timeline = pd.DataFrame(
        pd.date_range(start=start_date, end=end_date, freq=f'{freq_min}T'),
        columns=['timestamp']
    )
    timeline['hour_of_day'] = timeline['timestamp'].dt.hour
    timeline['day_of_week'] = timeline['timestamp'].dt.dayofweek
    timeline['day_of_year'] = timeline['timestamp'].dt.dayofyear
    return timeline

def simulate_weather(df):
    """Simulates realistic outside temperature and weather conditions for a tropical climate."""
    print("Simulating weather patterns...")
    # Seasonal pattern (sine wave over the year)
    seasonal_effect = 1.5 * np.sin(2 * np.pi * df['day_of_year'] / 365.25)
    
    # Daily pattern (sine wave over 24 hours)
    daily_effect = 4 * np.sin(2 * np.pi * df['hour_of_day'] / 24)
    
    # Base temp for Putrajaya, Malaysia + patterns + random noise
    df['outside_temp'] = 28 + seasonal_effect + daily_effect + np.random.normal(0, 0.5, len(df))
    df['outside_humidity'] = np.clip(75 + (df['outside_temp'] - 28) * 5 + np.random.normal(0, 5, len(df)), 60, 95)
    
    # Simple weather condition simulation
    conditions = ['sunny', 'cloudy', 'rainy']
    probs = [0.6, 0.3, 0.1] # Base probabilities
    df['weather_condition'] = np.random.choice(conditions, size=len(df), p=probs)
    return df

def simulate_occupancy(df):
    """Simulates room occupancy based on time-based patterns."""
    print("Simulating room occupancy...")
    occupancy = []
    for _, row in df.iterrows():
        is_weekday = row['day_of_week'] < 5
        if is_weekday:
            prob, max_occ = WEEKDAY_OCCUPANCY_PROB[row['hour_of_day']]
            if np.random.rand() < prob:
                occupancy.append(np.random.randint(1, max_occ + 1))
            else:
                occupancy.append(0)
        else: # Weekend
            if np.random.rand() < WEEKEND_OCCUPANCY_PROB:
                occupancy.append(np.random.randint(1, 3))
            else:
                occupancy.append(0)
    
    df['occupancy_count'] = occupancy
    df['is_occupied'] = (df['occupancy_count'] > 0).astype(int)
    return df

def simulate_room_thermodynamics(df):
    """Simulates indoor temperature based on all external and internal factors."""
    print("Simulating room thermodynamics and AC control...")
    room_temps = []
    ac_power_states = []
    
    # Initial state
    current_temp = 26.0
    ac_on = False

    for _, row in df.iterrows():
        # Heat transfer with outside
        temp_delta = (row['outside_temp'] - current_temp) * HEAT_TRANSFER_COEFFICIENT
        
        # Heat from occupants
        temp_delta += row['occupancy_count'] * HEAT_FROM_OCCUPANT
        
        # Simulated thermostat logic
        if row['is_occupied'] and current_temp > COMFORT_TEMP_MAX:
            ac_on = True
        elif current_temp < COMFORT_TEMP_MIN:
            ac_on = False
        elif not row['is_occupied']:
            ac_on = False
            
        # Cooling from AC
        if ac_on:
            temp_delta -= AC_COOLING_POWER
            
        # Update temperature with some sensor noise
        current_temp += temp_delta + np.random.normal(0, 0.05)
        
        room_temps.append(current_temp)
        ac_power_states.append(1 if ac_on else 0)

    df['room_temp'] = room_temps
    df['ac_power'] = ac_power_states
    # Add the AC's target temp for context
    df['ac_target_temp'] = COMFORT_TEMP_MIN 
    return df

def generate_time_to_cool_dataset(df):
    """Processes the main timeline to find and measure cooling cycles."""
    print("Generating Time-to-Cool training dataset by detecting cooling events...")
    cooling_events = []
    is_cooling_cycle = False
    cycle_start_info = {}

    for i, row in df.iterrows():
        # Detect start of a cooling cycle
        if not is_cooling_cycle and row['ac_power'] == 1 and row['room_temp'] > row['ac_target_temp']:
            is_cooling_cycle = True
            cycle_start_info = {
                'start_timestamp': row['timestamp'],
                'start_temp': row['room_temp'],
                'target_temp': row['ac_target_temp'],
                'outside_temp': row['outside_temp'],
                'outside_humidity': row['outside_humidity'],
                'weather_condition': row['weather_condition'],
                'time_of_day': row['hour_of_day']
            }
        
        # Detect end of a cooling cycle
        elif is_cooling_cycle and row['room_temp'] <= cycle_start_info['target_temp']:
            duration_minutes = (row['timestamp'] - cycle_start_info['start_timestamp']).total_seconds() / 60
            
            # Only save realistic cycles (e.g., more than 5 mins, less than 2 hours)
            if 5 < duration_minutes < 120:
                event = cycle_start_info.copy()
                event['time_to_cool_minutes'] = duration_minutes
                cooling_events.append(event)
            
            is_cooling_cycle = False

        # Discard cycle if AC was turned off manually before reaching target
        elif is_cooling_cycle and row['ac_power'] == 0:
            is_cooling_cycle = False

    return pd.DataFrame(cooling_events)

# --- Main Script Execution ---
if __name__ == "__main__":
    # 1. Generate the main, high-resolution timeline of events
    main_df = generate_base_timeline(DATA_START_DATE, DATA_END_DATE, TIME_FREQUENCY_MIN)
    main_df = simulate_weather(main_df)
    main_df = simulate_occupancy(main_df)
    main_df = simulate_room_thermodynamics(main_df)

    # 2. Prepare and save the dataset for the Smart Temperature Control Model
    print("\nSaving dataset for Temperature Control Model...")
    temp_control_df = main_df.copy()
    # Add cyclical time features as they are very useful for ML models
    # temp_control_df['sin_hour'] = np.sin(2 * np.pi * temp_control_df['hour_of_day'] / 24)
    # temp_control_df['cos_hour'] = np.cos(2 * np.pi * temp_control_df['hour_of_day'] / 24)
    temp_control_df.to_csv("smart_temp_control_data.csv", index=False)
    print("Dataset saved as 'smart_temp_control_data.csv'")
    print(temp_control_df.head())

    # # 3. Prepare and save the dataset for the Occupancy Prediction Model
    # print("\nSaving dataset for Occupancy Prediction Model...")
    # occupancy_df = main_df[['timestamp', 'is_occupied', 'day_of_week', 'hour_of_day']].copy()
    # occupancy_df.to_csv("occupancy_prediction_data.csv", index=False)
    # print("Dataset saved as 'occupancy_prediction_data.csv'")
    # print(occupancy_df.head())

    # # 4. Prepare and save the dataset for the Time-to-Cool Model
    # time_to_cool_df = generate_time_to_cool_dataset(main_df)
    # if not time_to_cool_df.empty:
    #     time_to_cool_df.to_csv("time_to_cool_data.csv", index=False)
    #     print("\nSaving dataset for Time-to-Cool Model...")
    #     print(f"Detected and created {len(time_to_cool_df)} cooling cycle events.")
    #     print("Dataset saved as 'time_to_cool_data.csv'")
    #     print(time_to_cool_df.head())
    # else:
    #     print("\nCould not generate Time-to-Cool dataset. Try adjusting simulation parameters.")

    print("\nData generation complete!")