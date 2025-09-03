import pandas as pd
import numpy as np
import datetime

# --- CONFIGURATION PARAMETERS ---

# Time settings
DATA_START_DATE = "2024-01-01"
DATA_END_DATE = "2024-12-31"
TIME_FREQUENCY_MIN = 5

# Room thermal properties
HEAT_TRANSFER_COEFFICIENT = 0.05
HEAT_FROM_OCCUPANT = 0.1
AC_MAX_COOLING_POWER = 1.8  # A very powerful AC unit, as specified

# Smart AC & Fan Control Parameters
AC_TEMP_SETTING_MIN = 22.0
AC_TEMP_SETTING_HIGH = 23.5
AC_TEMP_SETTING_ECO = 24.5
FAN_COOLING_EFFECT = {'off': 0.0, 'low': 0.08, 'medium': 0.15, 'high': 0.25}

# --- NEW: Realistic Power Consumption Model (in Kilowatts) ---
POWER_CONSUMPTION_KW = {
    'compressor': 1.5,   # Power draw when the compressor is actively cooling
    'fan_off': 0.0,
    'fan_low': 0.05,     # Fan-only mode for maintenance
    'fan_medium': 0.1,
    'fan_high': 0.2
}

# Occupancy patterns
WEEKDAY_OCCUPANCY_PROB = {
    **{h: (0.0, 0) for h in range(0, 8)}, 8: (0.2, 20), 9: (0.8, 20), 10: (0.9, 20),
    11: (0.9, 20), 12: (0.2, 20), 13: (0.5, 20), 14: (0.7, 20), 15: (0.5, 20),
    16: (0.5, 20), 17: (0.1, 20), 18: (0.05, 20), **{h: (0.0, 0) for h in range(19, 24)},
}
WEEKEND_OCCUPANCY_PROB = 0.05

# Thermostat simulation logic
COMFORT_TEMP_MAX = 25.0
COMFORT_TEMP_MIN = 23.0

# --- DATA GENERATION FUNCTIONS (Unchanged) ---
def generate_base_timeline(start_date, end_date, freq_min):
    print(f"Generating timeline from {start_date} to {end_date}...")
    timeline = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq=f'{freq_min}T'), columns=['timestamp'])
    timeline['hour_of_day'] = timeline['timestamp'].dt.hour; timeline['day_of_week'] = timeline['timestamp'].dt.dayofweek; timeline['day_of_year'] = timeline['timestamp'].dt.dayofyear
    return timeline

def simulate_weather(df):
    print("Simulating weather patterns...")
    seasonal_effect = 1.5 * np.sin(2 * np.pi * df['day_of_year'] / 365.25); daily_effect = -4 * np.cos(2 * np.pi * (df['hour_of_day'] - 2) / 24)
    df['outside_temp'] = 28 + seasonal_effect + daily_effect + np.random.normal(0, 0.2, len(df))
    df['outside_humidity'] = np.clip(75 + (df['outside_temp'] - 28) * 5 + np.random.normal(0, 5, len(df)), 60, 95)
    conditions = ['sunny', 'cloudy', 'rainy']
    day_mask = (df['hour_of_day'] >= 7) & (df['hour_of_day'] <= 18)
    df.loc[day_mask, 'weather_condition'] = np.random.choice(conditions, size=day_mask.sum(), p=[0.6, 0.3, 0.1])
    df.loc[~day_mask, 'weather_condition'] = np.random.choice(conditions[1:], size=(~day_mask).sum(), p=[0.7, 0.3])
    return df

def simulate_occupancy(df):
    print("Simulating room occupancy...")
    occupancy = np.zeros(len(df)); occupancy_duration_steps = 0; current_occupants = 0
    for i, row in df.iterrows():
        if occupancy_duration_steps > 0:
            occupancy[i] = current_occupants; occupancy_duration_steps -= 1
        else:
            current_occupants = 0; occupancy[i] = 0; is_weekday = row['day_of_week'] < 5
            if is_weekday:
                prob, max_occ = WEEKDAY_OCCUPANCY_PROB[row['hour_of_day']]
                if np.random.rand() < prob and max_occ > 0:
                    current_occupants = np.random.randint(1, max_occ + 1); session_length_minutes = np.random.uniform(30, 240)
                    occupancy_duration_steps = int(session_length_minutes / TIME_FREQUENCY_MIN); occupancy[i] = current_occupants
            else:
                if np.random.rand() < WEEKEND_OCCUPANCY_PROB:
                    current_occupants = np.random.randint(1, 3); session_length_minutes = np.random.uniform(30, 120)
                    occupancy_duration_steps = int(session_length_minutes / TIME_FREQUENCY_MIN); occupancy[i] = current_occupants
    df['occupancy_count'] = occupancy; df['is_occupied'] = (df['occupancy_count'] > 0).astype(int)
    return df

def simulate_room_thermodynamics(df):
    """
    Simulates thermodynamics with a realistic power consumption model.
    """
    print("Simulating room thermodynamics with detailed power consumption...")
    room_temps = []
    power_draws_kw = [] # REPLACES ac_power_states
    ac_reasons = []
    fan_speeds = []
    ac_temp_settings = []

    current_temp = 26.0
    compressor_on = False

    for _, row in df.iterrows():
        # --- 1. SMART CONTROL DECISION LOGIC (Same logic, determines state) ---
        if not row['is_occupied']:
            compressor_on = False; fan_speed = 'off'; ac_temp_setting = np.nan
            reason = "SYSTEM OFF: Room unoccupied"
        elif current_temp > COMFORT_TEMP_MAX:
            compressor_on = True
            if current_temp > COMFORT_TEMP_MAX + 1.5:
                fan_speed = 'high'; ac_temp_setting = AC_TEMP_SETTING_MIN; reason = "ACTION: Aggressive cooling (very hot)"
            elif current_temp > COMFORT_TEMP_MAX + 0.5:
                fan_speed = 'medium'; ac_temp_setting = AC_TEMP_SETTING_HIGH; reason = "ACTION: Normal cooling (warm)"
            else:
                fan_speed = 'low'; ac_temp_setting = AC_TEMP_SETTING_ECO; reason = "ACTION: Gentle cooling (slightly warm)"
        elif current_temp >= COMFORT_TEMP_MIN and current_temp <= COMFORT_TEMP_MAX:
            compressor_on = False; fan_speed = 'low'; ac_temp_setting = np.nan
            reason = "MAINTAIN: Temp in comfort zone, circulating air"
        else: # current_temp < COMFORT_TEMP_MIN
            compressor_on = False; fan_speed = 'off'; ac_temp_setting = np.nan
            reason = "SYSTEM OFF: Temp below comfort min"

        # --- 2. CALCULATE POWER CONSUMPTION FOR THE CURRENT STATE ---
        current_power = POWER_CONSUMPTION_KW[f'fan_{fan_speed}']
        if compressor_on:
            current_power += POWER_CONSUMPTION_KW['compressor']
        
        # --- 3. CALCULATE TEMPERATURE CHANGE ---
        temp_delta = (row['outside_temp'] - current_temp) * HEAT_TRANSFER_COEFFICIENT
        temp_delta += row['occupancy_count'] * HEAT_FROM_OCCUPANT
        if compressor_on:
            base_cooling = AC_MAX_COOLING_POWER * ((AC_TEMP_SETTING_ECO - ac_temp_setting) / (AC_TEMP_SETTING_ECO - AC_TEMP_SETTING_MIN))
            total_cooling = base_cooling + FAN_COOLING_EFFECT[fan_speed]
            temp_delta -= total_cooling

        # --- 4. UPDATE STATE FOR NEXT ITERATION ---
        current_temp += temp_delta + np.random.normal(0, 0.05)
        
        room_temps.append(current_temp)
        power_draws_kw.append(current_power)
        ac_reasons.append(reason)
        fan_speeds.append(fan_speed)
        ac_temp_settings.append(ac_temp_setting)

    df['room_temp'] = room_temps
    df['power_kw'] = power_draws_kw
    df['fan_speed'] = fan_speeds
    df['ac_temp_setting'] = ac_temp_settings
    df['ac_control_reason'] = ac_reasons
    return df

# --- Main Script Execution ---
if __name__ == "__main__":
    main_df = generate_base_timeline(DATA_START_DATE, DATA_END_DATE, TIME_FREQUENCY_MIN)
    main_df = simulate_weather(main_df)
    main_df = simulate_occupancy(main_df)
    main_df = simulate_room_thermodynamics(main_df)

    print("\nSaving dataset for Final Advanced HVAC Model...")
    main_df.to_csv("smart_hvac_control_data_v7_final.csv", index=False)
    print("Dataset saved as 'smart_hvac_control_data_v7_final.csv'")

    print("\n--- Sample of Final Data with Detailed Power Consumption ---")
    maintain_examples = main_df[main_df['ac_control_reason'].str.contains("MAINTAIN")]
    if not maintain_examples.empty:
        first_maintain_idx = maintain_examples.index[0]
        start_idx = max(0, first_maintain_idx - 5)
        end_idx = min(len(main_df), first_maintain_idx + 5)
        print("Note the change in 'power_kw' when compressor turns off but fan stays on:")
        print(main_df.loc[start_idx:end_idx][['timestamp', 'room_temp', 'power_kw', 'fan_speed', 'ac_control_reason']])
    else:
        print("No 'MAINTAIN' state examples found in the first few rows.")

    print("\nData generation complete!")