# 0. Requirements
# pip install lightgbm pandas scikit-learn

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import warnings
import joblib
warnings.filterwarnings('ignore')

# ---------- 1) load and basic cleaning ----------
PATH = 'machine_learning/models/time_to_cool_model/dataset.csv'   # update filename; your paste looks TAB-separated
TARGET_TEMP = 23.0
MAX_HORIZON_MIN = 240      # treat >4h as censored

df = pd.read_csv(PATH, sep=',', parse_dates=['timestamp'], dayfirst=True)
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True, errors='coerce')
df = df.sort_values('timestamp').reset_index(drop=True)

# quick fixes
df['power_kw'] = pd.to_numeric(df['power_kw'], errors='coerce').fillna(0.0)
df['fan_speed'] = df['fan_speed'].fillna('off').astype(str)
df['ac_control_reason'] = df['ac_control_reason'].fillna('').astype(str)
df['room_temp'] = pd.to_numeric(df['room_temp'], errors='coerce')

# compute median sampling cadence (minutes)
df['dt_min'] = df['timestamp'].diff().dt.total_seconds().div(60.0)
median_dt = df['dt_min'].median() if not df['dt_min'].isna().all() else 5.0
print('median cadence (min):', median_dt)
lag_5min = max(1, int(round(5.0 / median_dt)))   # how many rows ~= 5 minutes

# ---------- 2) AC "on" heuristic ----------
df['ac_on'] = (df['power_kw'] > 0.05) | (df['fan_speed'].str.lower() != 'off') \
              | df['ac_control_reason'].str.contains('cool', case=False, na=False) \
              | ((pd.to_numeric(df['ac_temp_setting'], errors='coerce').notnull()) &
                 (pd.to_numeric(df['ac_temp_setting'], errors='coerce') < df['room_temp']))

# ---------- 3) create labels: time_to_cool_min and censored ----------
temps = df['room_temp'].values
n = len(df)
time_to_cool = np.full(n, np.nan)
censored = np.zeros(n, dtype=bool)

# precompute indices where temp <= TARGET
target_idxs = np.where(temps <= TARGET_TEMP)[0]

# Vectorized-ish forward search (simple loop but using target_idxs to limit checks)
for i in range(n):
    if np.isnan(temps[i]):
        time_to_cool[i] = np.nan
        censored[i] = True
        continue
    if temps[i] <= TARGET_TEMP:
        time_to_cool[i] = 0.0
        continue
    # find first target index after i
    later_targets = target_idxs[target_idxs > i]
    if later_targets.size == 0:
        time_to_cool[i] = float(MAX_HORIZON_MIN)
        censored[i] = True
        continue
    j = later_targets[0]
    delta_min = (df.loc[j, 'timestamp'] - df.loc[i, 'timestamp']).total_seconds() / 60.0
    if delta_min > MAX_HORIZON_MIN:
        time_to_cool[i] = float(MAX_HORIZON_MIN)
        censored[i] = True
        continue
    # only label as success if AC was on at some point during [i .. j]
    if df.loc[i:j, 'ac_on'].any():
        time_to_cool[i] = float(delta_min)
    else:
        # no cooling observed even though temperature later <= target (maybe overnight) -> treat as censored
        time_to_cool[i] = float(MAX_HORIZON_MIN)
        censored[i] = True

df['time_to_cool_min'] = time_to_cool
df['censored'] = censored

print('Labeled rows:', (~df['censored']).sum(), 'Censored rows:', df['censored'].sum())

# ---------- 4) feature engineering ----------
# basic state
df['temp_diff'] = df['room_temp'] - TARGET_TEMP

# lag / cooling rate (use lag_5min computed above)
df['temp_lag_5'] = df['room_temp'].shift(lag_5min)
df['time_lag_5_min'] = (df['timestamp'] - df['timestamp'].shift(lag_5min)).dt.total_seconds().div(60.0)
# cooling_rate = (past_temp - current_temp) / minutes  => positive when cooling
df['cooling_rate_5min'] = (df['temp_lag_5'] - df['room_temp']) / df['time_lag_5_min']
df['cooling_rate_5min'] = df['cooling_rate_5min'].fillna(0.0)

# rolling stats (last 3 samples -> ~15 mins if cadence 5 min)
win = max(1, int(round(15.0 / median_dt)))
df['room_temp_roll_mean_15'] = df['room_temp'].rolling(window=win, min_periods=1).mean()
df['power_kw_roll_15'] = df['power_kw'].rolling(window=win, min_periods=1).mean()
df['ac_on_frac_15'] = df['ac_on'].rolling(window=win, min_periods=1).mean()

# fan speed numeric (map common strings)
fan_map = {'off': 0, 'low': 1, 'medium': 2, 'med': 2, 'high': 3}
df['fan_speed_num'] = df['fan_speed'].str.lower().map(fan_map)
df['fan_speed_num'] = pd.to_numeric(df['fan_speed_num'], errors='coerce').fillna(0)

# cyclic time features
df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24.0)
df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24.0)

# one-hot weather (small cardinality)
weather_dummies = pd.get_dummies(df['weather_condition'].fillna('unknown').astype(str), prefix='weather')
df = pd.concat([df, weather_dummies], axis=1)
df = df.drop(columns=['weather_condition'])

# select features
FEATURES = [
    'room_temp', 'temp_diff', 'cooling_rate_5min', 'room_temp_roll_mean_15',
    'outside_temp', 'outside_humidity', 'occupancy_count', 'is_occupied',
    'power_kw', 'power_kw_roll_15', 'fan_speed_num', 'ac_temp_setting',
    'hour_sin', 'hour_cos', 'ac_on_frac_15'
] + [c for c in df.columns if c.startswith('weather_')]

df_features = df[FEATURES + ['time_to_cool_min', 'censored']].copy()
df_features = df_features.dropna(subset=['time_to_cool_min'])   # drop rows with missing label

# Option: drop censored rows for initial regression training
trainable = df_features[~df_features['censored']].copy()
print('Trainable rows (non-censored):', len(trainable))

# ---------- 5) time-aware train/val/test split ----------
# use last 15% as test
trainable = trainable.reset_index(drop=True)
ntr = len(trainable)
train_end = int(ntr * 0.70)
val_end = int(ntr * 0.85)

X_train = trainable.loc[:train_end-1, FEATURES]
y_train = trainable.loc[:train_end-1, 'time_to_cool_min']
X_val = trainable.loc[train_end:val_end-1, FEATURES]
y_val = trainable.loc[train_end:val_end-1, 'time_to_cool_min']
X_test = trainable.loc[val_end:, FEATURES]
y_test = trainable.loc[val_end:, 'time_to_cool_min']

print('Train/Val/Test sizes:', len(X_train), len(X_val), len(X_test))

y_train = y_train.to_numpy(dtype=float)
y_val   = y_val.to_numpy(dtype=float)
y_test  = y_test.to_numpy(dtype=float)

# ---------- 6) Train LightGBM regressor ----------
model = lgb.LGBMRegressor(n_estimators=2000, learning_rate=0.05)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='l1',
    early_stopping_rounds=50,
    verbose=50
)

joblib.dump(model, "time_to_cool_model.pkl")

MODEL_PATH = "D:/Github/Pizza and Pasta Shop/SCADA-i/machine_learning/models/time_to_cool_model/time_to_cool_model.pkl"
joblib.dump(model, MODEL_PATH)
print("Model saved at:", MODEL_PATH)

# ---------- 7) Evaluate ----------
y_pred = model.predict(X_test)
print('MAE (min):', mean_absolute_error(y_test, y_pred))
print('RMSE:', mean_squared_error(y_test, y_pred))

# ---------- 8) Simple scheduling helper ----------
# two approaches:
#  A) If you only have current state and no forecast: estimate start_time = event_time - model.predict(now_features)
#  B) If you can simulate forecasted conditions: simulate candidate start times and pick the latest that still reaches target.

def predict_time_to_cool_row(row_df, model, features=FEATURES):
    x = row_df[features].values.reshape(1, -1)
    return float(model.predict(x)[0])

def recommend_start_simple(event_time, now_row, model):
    t_pred = predict_time_to_cool_row(now_row, model)
    start_time = pd.to_datetime(event_time) - pd.Timedelta(minutes=t_pred)
    return start_time, t_pred

# Example (use the latest row in df as "now")
now_row = df_features.iloc[-1:][FEATURES]
event_time = pd.to_datetime('2024-01-01 09:00')   # example event
start_time_guess, pred_minutes = recommend_start_simple(event_time, now_row, model)
print('If started now predicted minutes to cool:', pred_minutes)
print('Suggested start time (simple):', start_time_guess)

# Advanced: simulate candidate start times (requires forecast of outside/occupancy if start != now)
def find_latest_feasible_start(event_time, model, features_template, now_features, max_horizon=MAX_HORIZON_MIN, step_min=5):
    """
    If no forecast available, we assume outside/occupancy stay at now_features values.
    Searches backwards from event_time to find latest start that still achieves target.
    """
    event_time = pd.to_datetime(event_time)
    # generate candidate start times from (event_time - max_horizon) to event_time (latest-first)
    for offset in range(0, max_horizon+1, step_min):
        candidate_start = event_time - pd.Timedelta(minutes=offset)
        # build a candidate feature row: use now_features but you could replace some fields with forecasted ones
        candidate_features = now_features.copy()
        # optionally update any features that depend on start_time (none here)
        pred = predict_time_to_cool_row(candidate_features, model)
        if candidate_start + pd.Timedelta(minutes=pred) <= event_time:
            return candidate_start, pred
    return None, None

cand_start, cand_pred = find_latest_feasible_start(event_time, model, FEATURES, now_row)
print('latest feasible start (simulation, assume current conditions):', cand_start, 'pred min:', cand_pred)
