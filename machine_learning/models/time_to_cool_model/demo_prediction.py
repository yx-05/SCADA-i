import pandas as pd
import numpy as np
import joblib

# ---------- Load model ----------
MODEL_PATH = "D:/Github/Pizza and Pasta Shop/SCADA-i/machine_learning/models/time_to_cool_model/time_to_cool_model.pkl"
model = joblib.load(MODEL_PATH)

# ---------- Example input ----------
example_row = {
    'timestamp': '2024-01-01 08:30',
    'hour_of_day': 8,
    'day_of_week': 1,
    'day_of_year': 1,
    'outside_temp': 32,
    'outside_humidity': 50,
    'weather_condition': 'clear',
    'occupancy_count': 3,
    'is_occupied': 1,
    'room_temp': 28.5,
    'power_kw': 1.2,
    'fan_speed': 'medium',
    'ac_temp_setting': 23,
    'ac_control_reason': 'cooling'
}

df = pd.DataFrame([example_row])

# ---------- Feature engineering ----------
TARGET_TEMP = 23.0
df['temp_diff'] = df['room_temp'] - TARGET_TEMP
df['cooling_rate_5min'] = 0.0
df['room_temp_roll_mean_15'] = df['room_temp']
df['power_kw_roll_15'] = df['power_kw']

# Fan speed numeric
fan_map = {'off': 0, 'low': 1, 'medium': 2, 'med': 2, 'high': 3}
df['fan_speed_num'] = df['fan_speed'].str.lower().map(fan_map).fillna(0)

# Cyclic time features
df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24.0)
df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24.0)

# AC on fraction
df['ac_on_frac_15'] = ((df['power_kw'] > 0.05) |
                       (df['fan_speed_num'] > 0) |
                       df['ac_control_reason'].str.contains('cool', case=False, na=False)).astype(float)

# ---------- One-hot weather (ensure same columns as model) ----------
weather_dummies = pd.get_dummies(df['weather_condition'].fillna('unknown'), prefix='weather')

# Get the weather columns expected by the model
model_weather_cols = [c for c in model.feature_name_ if c.startswith('weather_')]

# Add missing weather columns as 0
for col in model_weather_cols:
    if col not in weather_dummies:
        weather_dummies[col] = 0

# Reorder columns to match model
weather_dummies = weather_dummies[model_weather_cols]

df = pd.concat([df, weather_dummies], axis=1)

# ---------- Select features ----------
FEATURES = model.feature_name_  # exact features from trained model

# ---------- Prediction ----------
t_pred = float(model.predict(df[FEATURES])[0])
print(f"Predicted time to reach {TARGET_TEMP}°C: {t_pred:.1f} minutes")
