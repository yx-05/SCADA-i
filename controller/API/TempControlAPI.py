import pandas as pd
import numpy as np
import joblib
import logging

class TempControlAPI:
    # The exact order of columns the model was trained on
    MODEL_COLUMNS = [
        'room_temp', 'outside_temp', 'weather_condition', 'is_peak_hour',
        'temp_diff', 'set_point_diff', 'hour_sin', 'hour_cos',
        'dayofweek_sin', 'dayofweek_cos'
    ]
    
    def __init__(self, MODEL_PATH):
        self.MODEL_PATH = MODEL_PATH
        self.model = None
        self.check_initialization()
    
    def check_initialization(self):
        try:
            self.model = joblib.load(self.MODEL_PATH)
        except FileNotFoundError:
            self.model = None
            logging.error(f'ERROR (TempControlAPI): "{self.MODEL_PATH}" not found')
    
    def predict(self, data):
        """
        Perform prediction of the given data.

        Args:
            data (dict): A dictionary representing the data point.
            
        Returns:
            value (float): The predicted value.
        """
        if self.model == None:
            logging.error("ERROR (TempControlAPI): Model not found!")
            return None
            
        if data is None or (hasattr(data, "empty") and data.empty):
            logging.error("ERROR (TempControlAPI): Data not found")
            return None

        try:
            # Preprocess the data
            processed_df = self._preprocess_data(data)

            # Run prediction
            prediction = self.model.predict(processed_df)
            
            return prediction

        except (ValueError, KeyError) as e:
            logging.error("ERROR (TempControlAPI): Data preprocessing error")
            return None
        except Exception as e:
            logging.error(f"ERROR (TempControlAPI): {e}")
            return None
        
    def _preprocess_data(self, data):
        """
        Performs all necessary preprocessing on the input data.
        Ensures robust handling of missing values and schema mismatches.
        """
        df = pd.DataFrame(data)

        # Use only last row if enough history is present
        if len(df) >= 4:
            df = df.iloc[[-1]]

        # --- Required Columns Validation ---
        required_cols = ["timestamp", "room_temp", "outside_temp", "ac_temp_setting", "weather_condition"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required input columns: {missing}")

        # --- Time Features ---
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        if df["timestamp"].isnull().any():
            raise ValueError("Invalid or missing timestamp")
        df["hour"] = df["timestamp"].dt.hour
        df["dayofweek"] = df["timestamp"].dt.dayofweek
        df["is_peak_hour"] = df["hour"].between(12, 17).astype(int)

        # --- Cyclical Features ---
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)
        df["dayofweek_sin"] = np.sin(2 * np.pi * df["dayofweek"] / 7.0)
        df["dayofweek_cos"] = np.cos(2 * np.pi * df["dayofweek"] / 7.0)

        # --- Engineered Features ---
        df["temp_diff"] = df["room_temp"].fillna(method="ffill").fillna(25) - \
                        df["outside_temp"].fillna(method="ffill").fillna(30)

        df["set_point_diff"] = df["room_temp"].fillna(method="ffill").fillna(25) - \
                            df["ac_temp_setting"].fillna(df["ac_temp_setting"].mean()).fillna(24)

        # --- Drop unused columns safely ---
        columns_to_drop = [
            "day_of_year", "occupancy_count", "is_occupied",
            "outside_humidity", "timestamp", "hour_of_day",
            "day_of_week", "ac_control_reason"
        ]
        df.drop(columns=[c for c in columns_to_drop if c in df.columns], inplace=True)

        # --- Ensure correct order ---
        final_df = df.reindex(columns=self.MODEL_COLUMNS)

        # --- Final NaN Check ---
        if final_df.isnull().any().any():
            raise ValueError(f"NaNs remain in processed data: {final_df.isnull().sum()}")

        return final_df