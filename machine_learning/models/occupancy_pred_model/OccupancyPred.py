import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

class OccupancyPred:
    def __init__(self, model_path):
        # Load trained ML model
        self.model = joblib.load(model_path)

        # Label encoder for weather
        self.le_weather = LabelEncoder()
        self.le_weather.fit(["cloudy", "rainy", "sunny"])

    def _encode_cyclical(self, df, col, max_val):
        df[col + "_sin"] = np.sin(2 * np.pi * df[col] / max_val)
        df[col + "_cos"] = np.cos(2 * np.pi * df[col] / max_val)
        return df

    def _preprocess(self, df):
        """
        Expect at a new row and its 3 previous row for preprocessing
        """
        # Convert dict to DataFrame
        # df = pd.DataFrame([new_row])
        
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Time features
        df["month_of_year"] = df["timestamp"].dt.month
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

        # Lag features
        df["occ_lag1"] = df["is_occupied"].shift(1)
        df["occ_lag2"] = df["is_occupied"].shift(2)
        df["occ_lag3"] = df["is_occupied"].shift(3)

        df["temp_lag1"] = df["room_temp"].shift(1)
        df["temp_lag2"] = df["room_temp"].shift(2)

        # Rolling averages
        df["occ_rolling_mean_3"] = df["is_occupied"].rolling(window=3).mean()
        df["temp_rolling_mean_3"] = df["room_temp"].rolling(window=3).mean()

        # Cyclical features
        df = self._encode_cyclical(df, "hour_of_day", 24)
        df = self._encode_cyclical(df, "day_of_week", 7)

        # Encode weather
        df["weather_encoded"] = self.le_weather.transform(df["weather_condition"])

        # Select last row (current prediction input)
        df = df.drop(["timestamp", "weather_condition", "is_occupied", "occupancy_count", "ac_control_reason", "power_kw", "fan_speed", "ac_temp_setting"], axis=1)

        return df.iloc[[-1]]

    def predict(self, df):
        """
        Runs preprocessing + prediction
        """
        features = self._preprocess(df)

        prediction = self.model.predict_proba(features)
        return prediction[0][1]

# Notes
"""
For real deployment need to take care of missing value.
Implement error handling for less than 4 rows
"""