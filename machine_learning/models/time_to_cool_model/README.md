# Time-to-Cool Model
[![Python Version](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)

## Overview
Predict how long it will take for a room to reach a target temperature (e.g., 23°C) and recommend the optimal time to start pre-cooling, based on historical HVAC and environmental data.
---
## Files
- `time_to_cool.ipynb` → Complete model training pipeline
- `demo_prediction.py` → Simulation of predictions
- `dataset.csv` → Test data for simulation of predictions
---
# Installation 
Navigate to this module folder:
```bash
cd time_to_cool_model
pip install -r requirements.txt
```
Libraries for training and running will be downloaded.
---
# Running
To simulate the retreiving of data from database and run the preditions, demo_prediction.py is created. To run the file make sure the python environment is installed with the required libraries. Also make sure that dataset.csv files are configured to the correct path.
---
# Input
`dataset.csv` → 105121 rows of generated input dataset for prediction
---
# Output
```bash
Predicted time to reach 23.0°C: 101.4 minutes
```
