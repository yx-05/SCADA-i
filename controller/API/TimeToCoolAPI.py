import pandas as pd
import numpy as np
import lightgbm as lgb
import joblib  # Make sure joblib is imported
import warnings

warnings.filterwarnings('ignore')

class TimeToCoolAPI:
    """
    A class to predict the time to cool a room based on a pre-trained LightGBM model.
    This class can load both native LightGBM .txt models and scikit-learn .pkl files.
    """

    def __init__(self, model_path='time_to_cool_model.pkl'): # Can be .pkl or .txt
        """
        Initializes the TimeToCoolPredictor. It tries to load a native LGBM model first,
        then falls back to loading a joblib .pkl file and extracting the core booster.

        Args:
            model_path (str): The path to the saved model file.
        """
        self.model = None
        try:
            # First, try the best method: loading a native model
            self.model = lgb.Booster(model_file=model_path)
            print("Successfully loaded native LightGBM model.")
        except lgb.basic.LightGBMError:
            # If that fails, it's likely a .pkl file. Load it and extract the booster.
            print(f"Could not load native model. Falling back to load '{model_path}' as a .pkl file.")
            try:
                sklearn_model = joblib.load(model_path)
                # The core model is stored in the 'booster_' attribute
                self.model = sklearn_model.booster_
                print("Successfully loaded .pkl file and extracted the core model.")
            except Exception as e:
                print(f"Error loading model from {model_path}: {e}")
                raise IOError(f"Could not load the model from {model_path}. Please check the file and path.")

        if self.model is None:
            raise ValueError("Model could not be loaded.")

        self.features = [
            'room_temp', 'temp_diff', 'cooling_rate_5min', 'room_temp_roll_mean_15',
            'outside_temp', 'outside_humidity', 'occupancy_count', 'is_occupied',
            'power_kw', 'power_kw_roll_15', 'fan_speed_num', 'ac_temp_setting',
            'hour_sin', 'hour_cos', 'ac_on_frac_15', 'weather_cloudy', 'weather_rainy', 'weather_sunny'
        ]
        self.TARGET_TEMP = 23.0
        self.median_dt = 5.0
        
    def _preprocess(self, df):
        """
        Preprocesses the input DataFrame to generate features for the model.

        Args:
            df (pd.DataFrame): The input DataFrame with raw data.

        Returns:
            pd.DataFrame: The preprocessed DataFrame with features for prediction.
        """
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.sort_values('timestamp').reset_index(drop=True)

        # Handle missing and incorrect data types robustly
        df['power_kw'] = pd.to_numeric(df['power_kw'], errors='coerce').fillna(0.0)
        df['fan_speed'] = df['fan_speed'].fillna('off').astype(str)
        df['ac_temp_setting'] = pd.to_numeric(df['ac_temp_setting'], errors='coerce').fillna(self.TARGET_TEMP)
        df['room_temp'] = pd.to_numeric(df['room_temp'], errors='coerce')
        df['outside_temp'] = pd.to_numeric(df['outside_temp'], errors='coerce')
        df['outside_humidity'] = pd.to_numeric(df['outside_humidity'], errors='coerce')
        df['occupancy_count'] = pd.to_numeric(df['occupancy_count'], errors='coerce').fillna(0)
        df['is_occupied'] = pd.to_numeric(df['is_occupied'], errors='coerce').fillna(0)

        # Feature Engineering
        lag_5min = max(1, int(round(5.0 / self.median_dt)))
        
        df['ac_on'] = (df['power_kw'] > 0.05) | (df['fan_speed'].str.lower() != 'off')
        df['temp_diff'] = df['room_temp'] - self.TARGET_TEMP
        
        if len(df) == 1:
            df['temp_lag_5'] = df['room_temp']
            df['time_lag_5_min'] = 5.0
        else:
            df['temp_lag_5'] = df['room_temp'].shift(lag_5min)
            df['time_lag_5_min'] = (df['timestamp'] - df['timestamp'].shift(lag_5min)).dt.total_seconds().div(60.0)

        df['cooling_rate_5min'] = (df['temp_lag_5'] - df['room_temp']) / df['time_lag_5_min']
        df['cooling_rate_5min'] = df['cooling_rate_5min'].fillna(0.0)

        win = max(1, int(round(15.0 / self.median_dt)))
        df['room_temp_roll_mean_15'] = df['room_temp'].rolling(window=win, min_periods=1).mean()
        df['power_kw_roll_15'] = df['power_kw'].rolling(window=win, min_periods=1).mean()
        df['ac_on_frac_15'] = df['ac_on'].rolling(window=win, min_periods=1).mean()

        fan_map = {'off': 0, 'low': 1, 'medium': 2, 'med': 2, 'high': 3}
        df['fan_speed_num'] = df['fan_speed'].str.lower().map(fan_map)
        df['fan_speed_num'] = pd.to_numeric(df['fan_speed_num'], errors='coerce').fillna(0)

        df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24.0)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24.0)

        weather_dummies = pd.get_dummies(df['weather_condition'].fillna('unknown').astype(str), prefix='weather')
        df = pd.concat([df, weather_dummies], axis=1)

        for col in self.features:
            if col not in df.columns:
                df[col] = 0
        
        df[self.features] = df[self.features].fillna(0)
        return df

    def predict(self, data):
        """
        Makes a prediction on the time to cool based on the input data.
        """
        if isinstance(data, dict):
            input_df = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            input_df = data.copy()
        else:
            raise ValueError("Input data must be a dictionary or a pandas DataFrame.")
            
        preprocessed_df = self._preprocess(input_df)
        features_for_prediction = preprocessed_df[self.features]
        
        # Use the predict method from the core Booster object
        return self.model.predict(features_for_prediction)

# --- EXAMPLE USAGE ---
if __name__ == '__main__':
    # This will now work with your original 'time_to_cool_model.pkl' file
    predictor = TimeToCoolAPI(model_path='D:/Github/campus_bms/controller/models/time_to_cool_model.pkl')

    single_data_point = {
        'timestamp': '2024-01-01 00:00:00',
        'hour_of_day': 0,
        'day_of_week': 0,
        'day_of_year': 1,
        'outside_temp': 24.593342,
        'outside_humidity': 60.0,
        'weather_condition': 'cloudy',
        'occupancy_count': 0.0,
        'is_occupied': 0,
        'room_temp': 26.006586,
        'power_kw': 0.0,
        'fan_speed': 'off',
        'ac_temp_setting': None,
        'ac_control_reason': 'SYSTEM OFF: Room unoccupied'
    }

    prediction = predictor.predict(single_data_point)
    print(f"\nPredicted time to cool: {prediction[0]:.2f} minutes")
