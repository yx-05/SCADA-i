# 🪑 Occupancy Prediction Model

This model is train on a synthetic dataset with XGBoost classifier to predict the probability of occupancy after 30 minutes starting from a given time. 

---

## 💻 Model Training

The model was trained and tested using **Optuna** with **XGBoost**.

### 🔹**Occupancy Prediction Model (Classification)**

* **Algorithm:** `XGBoost`
* **Task:** Predict the occupancy probability for the next 1 hour.
* **Method:**

  * Pipeline (`preprocess → classifier`)
  * Hyperparameter tuning with `GridSearchCV`
  * Scoring metric: **F1-score**

---

## 🧠 Results

| Metric   | Score      |
| -------- | ---------- |
| F1 Score tuning with optuna | **0.86**  |
| F1 Score on unseen test set | **0.87**   |

---

## 📂 Project Files

```
temperature-control-model/
│── OccupancyPred.py  # A class that compiles the preprocessing and prediction code
│── model.ipynb # Complete model training Jupyter notebook
│── temperature_control.ipynb # Python notebook
│── occupancy_pred.ipynb # Exported model
|── run_example.py # Simulation of predictions
│── testset.csv # Test data for simulation of predictions
```

---

## 🚀 How to Use

### 1. Clone the repo

```bash
git clone https://github.com/yx-05/SCADA-i.git
cd SCADA-i/machine_learning/models/occupancy_pred_model
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run the notebook

```bash
jupyter notebook notebooks/model.ipynb
```

### 3. Run the simulation

To simulate retrieving data from the database and running predictions, run `run_example.py`. Ensure that your Python environment has all required libraries installed, and that `occupancy_pred.joblib` and `testset.csv` are correctly configured with the proper paths.
```bash
python run_example.py
```

---

## 📃 Example output
```bash
The probability of next 1 hours for occupancy is: 0.7208425
```
The prediction is based on the last 4 rows of the time series data. 

---

## 🔍 Explainability with SHAP

**SHAP (SHapley Additive exPlanations)** is applied to see which features matter most to the model.

📊 Example SHAP output:

* **Current occupied state** and **cosine of the current hour** → most important
* **Lag features for indoor temperature** → smaller effect

The next hour occupancy is going to be quite similar to the recent occupancy. While for the time features, converting it to cos making time around noon to be -1 and this explain why lower value in it possibly predict higher probability in occupancy, as people use the room usually during this time. 

---
