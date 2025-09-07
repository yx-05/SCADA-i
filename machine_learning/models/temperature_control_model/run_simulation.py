import joblib
import pandas as pd

loaded_fan_model = joblib.load('best_fan_model.joblib')
loaded_temp_model = joblib.load('best_temp_model.joblib')
loaded_power_model = joblib.load('best_power_model.joblib')

new_data = pd.read_csv("testing_data.csv")

fan_prediction = loaded_fan_model.predict(new_data)
temp_prediction = loaded_temp_model.predict(new_data)
power_prediction = loaded_power_model.predict(new_data)

print("New Fan Speed Predictions {0:high, 1:low, 2:medium, 3:off, 4:on}:", fan_prediction)
print("New AC Temperature Predictions:", temp_prediction)
print("New Power Consumption Predictions:", power_prediction)
