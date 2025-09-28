import pandas as pd
import numpy as np
import joblib
import logging

class OccupancyAPI:
    # The exact order of columns the model was trained on
    MODEL_COLUMNS = [
    'hour_of_day', 'day_of_week', 'day_of_year', 'outside_temp',
    'outside_humidity', 'is_occupied', 'room_temp', 'month_of_year',
    'is_weekend', 'occ_lag1', 'occ_lag2', 'occ_lag3', 'temp_lag1',
    'temp_lag2', 'occ_rolling_mean_3', 'temp_rolling_mean_3',
    'hour_of_day_sin', 'hour_of_day_cos', 'day_of_week_sin',
    'day_of_week_cos', 'weather_encoded'
    ]
    
    WEATHER_MAPPING = {'cloudy': 0, 'rainy': 1, 'clear': 2} 
    
    def __init__(self, MODEL_PATH):
        self.MODEL_PATH = MODEL_PATH
        self.model = None
        self.check_initialization()
    
    def check_initialization(self):
        try:
            self.model = joblib.load(self.MODEL_PATH)
        except FileNotFoundError:
            self.model = None
            logging.error(f'ERROR (OccupancyAPI): "{self.MODEL_PATH}" not found')
    
    def predict(self, data):
        """
        Perform prediction of the given data.

        Args:
            data (dict): A dictionary representing the data point.
            
        Returns:
            value (float): The predicted value.
        """
        if self.model == None:
            logging.error("ERROR (OccupancyAPI): Model not found!")
            return None
            
        if data is None or data.empty:
            logging.error("ERROR (OccupancyAPI): Data not found")
            return None
        
        if len(data) < 4:
            logging.warning("WARNING (OccupancyAPI): Not enough row of data to predict. Need at least 4 rows")

        try:
            # Preprocess the data
            processed_df = self._preprocess_data(data)

            # Run prediction
            prediction = self.model.predict(processed_df)
            
            return prediction

        except (ValueError, KeyError) as e:
            logging.error("ERROR (OccupancyAPI): Data preprocessing error")
            return None
        except Exception as e:
            logging.error(f"ERROR (OccupancyAPI): {e}")
            return None
    
    def _encode_cyclical(self, df, col, max_val):
        """Encodes a cyclical feature into sin and cos components."""
        df[col + '_sin'] = np.sin(2 * np.pi * df[col] / max_val)
        df[col + '_cos'] = np.cos(2 * np.pi * df[col] / max_val)
        return df

    def _preprocess_data(self, data):
        """
        Performs all necessary preprocessing on the input data.

        Args:
            current_data (dict): A dictionary representing the current data point.
            historical_data (list of dict): A list of the 3 most recent historical data points.
            
        Returns:
            pd.DataFrame: A preprocessed DataFrame ready for prediction.
        """
        df = pd.DataFrame(data)
        
        if len(df) < 4:
            df = pd.concat([df]*4, ignore_index=True)
            

        # --- Robustly handle potential null values in key columns ---
        # For this model, we'll forward-fill to handle missing sensor data robustly.
        # occupancy_count is dropped, but is_occupied is key for lags.
        df['is_occupied'] = df['is_occupied'].fillna(method='ffill')
        df['room_temp'] = df['room_temp'].fillna(method='ffill')

        # 2. Initial Column Dropping (as per notebook)
        cols_to_drop_initial = ["occupancy_count", "ac_control_reason", "power_kw", "fan_speed", "ac_temp_setting"]
        df = df.drop(columns=cols_to_drop_initial)

        # 3. Timestamp Feature Engineering
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['month_of_year'] = df['timestamp'].dt.month
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df = df.drop(columns='timestamp')

        # 4. Lag Feature Creation
        df['occ_lag1'] = df['is_occupied'].shift(1)
        df['occ_lag2'] = df['is_occupied'].shift(2)
        df['occ_lag3'] = df['is_occupied'].shift(3)
        df['temp_lag1'] = df['room_temp'].shift(1)
        df['temp_lag2'] = df['room_temp'].shift(2)

        # 5. Rolling Average Features
        df['occ_rolling_mean_3'] = df['is_occupied'].rolling(window=3, min_periods=1).mean()
        df['temp_rolling_mean_3'] = df['room_temp'].rolling(window=3, min_periods=1).mean()

        # The first few rows will have NaNs from shifts/rolling, which is expected.
        # We will only use the final, fully-featured row for prediction.
        df = df.dropna().reset_index(drop=True)

        if df.empty:
            raise ValueError("Preprocessing resulted in an empty DataFrame. Check for NaNs in input.")

        # 6. Cyclical Feature Encoding
        df = self._encode_cyclical(df, 'hour_of_day', 24)
        df = self._encode_cyclical(df, 'day_of_week', 7)

        # 7. Label Encode Weather Condition
        df['weather_encoded'] = df['weather_condition'].str.lower().map(self.WEATHER_MAPPING)
        if df['weather_encoded'].isnull().any():
            unknown_weather = df[df['weather_encoded'].isnull()]['weather_condition'].unique()
            raise ValueError(f"Unknown weather condition(s): {unknown_weather}. Expected one of {list(self.WEATHER_MAPPING.keys())}")

        df = df.drop(columns="weather_condition")

        # 8. Select the last row (current prediction) and ensure column order
        final_df = df.iloc[[-1]]

        # Ensure all required columns are present and in the correct order
        final_df = final_df.reindex(columns=self.MODEL_COLUMNS)
        
        if final_df.isnull().any().any():
            raise ValueError(f"Final preprocessed data has NaNs: "
                             f"{final_df.isnull().sum()[final_df.isnull().sum() > 0]}")

        return final_df