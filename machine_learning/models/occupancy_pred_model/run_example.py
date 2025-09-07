import pandas as pd
import os

from OccupancyPred import OccupancyPred

BASE_DIR = os.path.dirname(__file__)  # folder where current .py file lives
MODEL_PATH = os.path.join(BASE_DIR, "occupancy_pred.joblib")

model = OccupancyPred(MODEL_PATH)

# The input for the prediction have to be at least 4 row time series data
# Simulation of getting 4 rows of time series data from database
df = pd.read_csv("testset.csv")
df = df.iloc[-4:]

result = model.predict(df)

print("The probability of next 1 hours for occupancy is:", result)