# Occupancy Prediction Model
[![Python Version](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)

# Overview
This model is train on a synthetic dataset with XGBoost classifier to predict the probability of occupancy after 30 minutes starting from a given time.
The model score **0.8643** for F1-score tuning with optuna and get a overall F1-score of **0.88** for an unseen test dataset.

---

# Files
- `OccupancyPred.py` → A class that compiles the preprocessing and prediction code
- `model.ipynb` → complete model training pipeline
- `occupancy_pred.ipynb` → exported model
- `run_example.py` → simulation of predictions
- `testset.csv` → test data for simulation of predictions

---
# Installation 
Navigate to this module folder:
```bash
cd occupancy_pred_model
pip install -r requirements.txt
```
Libraries for training and running will be downloaded.

---
# Running
To simulate the retreiving of data from database and run the preditions, `run_example.py` is created. 
To run the file make sure the python environment is installed with the required libraries. Also make sure that `occupancy_pred.joblib` and `testset.csv` files are configured to the correct path. 

---
# Input
`testset.csv` → 20 rows of generated input dataset for prediction

---
# Output
```bash
The probability of next 30 mins for occupancy is: 0.6004461
```
The prediction is based on the last 4 rows of the time series data. 


