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
    # Hour: (Probability of new people arriving, Max occupants)
    **{h: (0.0, 0) for h in range(0, 8)},      # Night
    8: (0.3, 3), 9: (0.8, 5), 10: (0.9, 5), 11: (0.9, 5), # Morning
    12: (0.2, 5),                             # Lunch dip
    13: (0.7, 5), 14: (0.6, 5), 15: (0.5, 5), 16: (0.4, 5), # Afternoon
    17: (0.1, 3), 18: (0.05, 2),              # Evening
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
    """
    Simulates realistic outside temperature and weather conditions for a tropical climate.
    FIXED:
    - Daily temperature cycle now peaks in the afternoon (around 2 PM).
    - Reduced random noise for a smoother, more realistic temperature curve.
    - Weather conditions are now dependent on the time of day (no 'sunny' at night).
    """
    print("Simulating weather patterns...")
    # Seasonal pattern (sine wave over the year)
    seasonal_effect = 1.5 * np.sin(2 * np.pi * df['day_of_year'] / 365.25)

    # Daily pattern (cosine wave, shifted to peak at 14:00/2 PM)
    daily_effect = -4 * np.cos(2 * np.pi * (df['hour_of_day'] - 2) / 24)

    # Base temp for Putrajaya, Malaysia + patterns + REDUCED random noise
    df['outside_temp'] = 28 + seasonal_effect + daily_effect + np.random.normal(0, 0.2, len(df))
    df['outside_humidity'] = np.clip(75 + (df['outside_temp'] - 28) * 5 + np.random.normal(0, 5, len(df)), 60, 95)

    # --- Improved weather condition simulation ---
    conditions = ['sunny', 'cloudy', 'rainy']
    df['weather_condition'] = 'sunny' # Default value

    # Day time (7 AM to 6 PM)
    day_mask = (df['hour_of_day'] >= 7) & (df['hour_of_day'] <= 18)
    df.loc[day_mask, 'weather_condition'] = np.random.choice(conditions, size=day_mask.sum(), p=[0.6, 0.3, 0.1])

    # Night time
    night_mask = ~day_mask
    df.loc[night_mask, 'weather_condition'] = np.random.choice(conditions[1:], size=night_mask.sum(), p=[0.7, 0.3]) # Only cloudy or rainy

    return df

def simulate_occupancy(df):
    """
    Simulates room occupancy based on time-based patterns with more realism.
    FIXED:
    - Occupancy is now persistent. Instead of randomizing every 5 minutes, this
      function simulates "sessions" where occupants arrive and stay for a
      continuous period of time.
    """
    print("Simulating room occupancy...")
    occupancy = np.zeros(len(df))
    # This state variable will track how many more 5-min intervals the room will be occupied
    occupancy_duration_steps = 0
    current_occupants = 0

    for i, row in df.iterrows():
        if occupancy_duration_steps > 0:
            # If in an occupied session, continue it
            occupancy[i] = current_occupants
            occupancy_duration_steps -= 1
        else:
            # Reset and check if a new session should start
            current_occupants = 0
            occupancy[i] = 0
            is_weekday = row['day_of_week'] < 5
            
            if is_weekday:
                prob, max_occ = WEEKDAY_OCCUPANCY_PROB[row['hour_of_day']]
                if np.random.rand() < prob and max_occ > 0:
                    # Start a new occupancy session
                    current_occupants = np.random.randint(1, max_occ + 1)
                    # Stay for 30 mins to 4 hours (in 5-min steps)
                    session_length_minutes = np.random.uniform(30, 240)
                    occupancy_duration_steps = int(session_length_minutes / TIME_FREQUENCY_MIN)
                    occupancy[i] = current_occupants
            else: # Weekend
                if np.random.rand() < WEEKEND_OCCUPANCY_PROB:
                    # Start a new weekend occupancy session
                    current_occupants = np.random.randint(1, 3)
                    session_length_minutes = np.random.uniform(30, 120)
                    occupancy_duration_steps = int(session_length_minutes / TIME_FREQUENCY_MIN)
                    occupancy[i] = current_occupants

    df['occupancy_count'] = occupancy
    df['is_occupied'] = (df['occupancy_count'] > 0).astype(int)
    return df

def simulate_room_thermodynamics(df):
    """
    Simulates indoor temperature based on all external and internal factors.
    IMPROVED:
    - Added a new 'ac_control_reason' column to log *why* the AC state
      changes, providing much richer data for analysis.
    """
    print("Simulating room thermodynamics and AC control...")
    room_temps = []
    ac_power_states = []
    ac_reasons = [] # NEW: To store the reason for the AC state

    # Initial state
    current_temp = 26.0
    ac_on = False

    for i, row in df.iterrows():
        # Heat transfer with outside
        temp_delta = (row['outside_temp'] - current_temp) * HEAT_TRANSFER_COEFFICIENT

        # Heat from occupants
        temp_delta += row['occupancy_count'] * HEAT_FROM_OCCUPANT

        # --- Improved thermostat logic with detailed reasoning ---
        previous_ac_state = ac_on
        reason = f"UNCHANGED: {'Cooling' if ac_on else 'Off'}"

        if row['is_occupied'] and current_temp > COMFORT_TEMP_MAX and not ac_on:
            ac_on = True
            reason = "TURN ON: Occupied and temp > max comfort"
        elif ac_on and current_temp < COMFORT_TEMP_MIN:
            ac_on = False
            reason = "TURN OFF: Temp < min comfort"
        elif ac_on and not row['is_occupied']:
            # Handle case where room becomes unoccupied while AC is on
            if i > 0 and df.loc[i-1, 'is_occupied'] == 1:
                 ac_on = False
                 reason = "TURN OFF: Room is now unoccupied"

        # Cooling from AC
        if ac_on:
            temp_delta -= AC_COOLING_POWER

        # Update temperature with some sensor noise
        current_temp += temp_delta + np.random.normal(0, 0.05)

        room_temps.append(current_temp)
        ac_power_states.append(1 if ac_on else 0)
        ac_reasons.append(reason)

    df['room_temp'] = room_temps
    df['ac_power'] = ac_power_states
    df['ac_control_reason'] = ac_reasons # Add new reason column
    df['ac_target_temp'] = COMFORT_TEMP_MIN
    return df

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
    temp_control_df.to_csv("smart_temp_control_data_v2.csv", index=False)
    print("Dataset saved as 'smart_temp_control_data_v2.csv'")
    print("--- Sample of Final Data ---")
    print(temp_control_df.head())
    print("\n--- Sample of AC Control Log ---")
    # Show rows where the AC state changed to demonstrate the new reason log
    print(temp_control_df[temp_control_df['ac_control_reason'].str.contains("TURN")].head())

    print("\nData generation complete!")