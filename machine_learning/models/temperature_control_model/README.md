# 🌡️ AI Temperature Control System

This project builds an **AI system to optimize room temperature**.
It predicts **AC temperature settings, fan speed, and power usage** using past data like weather, occupancy, and room conditions.

The goal: **Save energy ⚡ while keeping rooms comfortable 😌**.

---

## 📊 Dataset

* **105k+ rows** of data with numerical and categorical data.
* Example row:

| Timestamp | Hour of day | Day of week | Day of year | Outside temp | Outside humidity | Weather condition | Occupany count | Is occupied | Room temp | Power kw | Fan speed | AC temp setting | AC control reason |  
| ---- | ------------ | -------- | --------- | --------- | --------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 2024-01-01  13:20:00    |   13   | 0    | 1       | 31.540126254344397   | 94.39886728711471  |cloudy |13.0 |1| 23.644217546112497    | 1.6|medium  | 22°C   | ACTION: Normal cooling (warm)   |

---

## 💻 Model Training

The model was trained and tested using **GridSearchCV + ML Pipelines** with **Random Forest** and **LightGBM**.

### 🔹 1. **Fan Speed Model (Classification)**

* **Algorithm:** `RandomForestClassifier`
* **Task:** Predict fan speed (categorical labels: e.g., Low, Medium, High).
* **Method:**

  * Pipeline (`preprocess → classifier`)
  * Hyperparameter tuning with `GridSearchCV`
  * Scoring metric: **F1 (weighted)**

---

### 🔹 2. **AC Temperature Model (Regression)**

* **Algorithm:** `RandomForestRegressor`
* **Task:** Predict AC temperature setting (continuous numeric values).
* **Method:**

  * Pipeline (`preprocess → regressor`)
  * Hyperparameter tuning with `GridSearchCV`
  * Scoring metric: **R²**

---

### 🔹 3. **Power Consumption Model (Regression)**

* **Algorithm:** `LGBMRegressor` 
* **Task:** Predict power usage (continuous numeric values).
* **Method:**

  * Pipeline (`preprocess → regressor`)
  * Hyperparameter tuning with `GridSearchCV`
  * Scoring metric: **R²**

---

## 🧠 Results

| Task                   | Metric   | Score      |
| ---------------------- | -------- | ---------- |
| Fan Speed Prediction   | Accuracy | **0.9999295179024528**  |
|                        | F1 Score | **0.999929541864823**   |
| AC Temp Prediction     | RMSE     | **0.0023704850419352073** |
|                        | R² Score | **0.9999884409470046**   |
| Power Usage Prediction | RMSE     | **0.03125434962233065**   |
|                        | R² Score | **0.9840074780487902**   |

---

## 📂 Project Files

```
temperature-control-model/
│── dataset.csv  # Dataset
│── testing_data.csv # Testing Dataset
│── temperature_control.ipynb # Python Notebook
│── best_temp_model.joblib # Saved temperature model
|── best_fan_model.joblib # Saved fan model
|── best_power_model.joblib # Saved power model
│── requirements.txt # Necessary package dependencies
│── README.md
```

---

## 🚀 How to Use

### 1. Clone the repo

```bash
git clone https://github.com/yx-05/SCADA-i.git
cd SCADA-i/machine_learning/models/temperature_control_model
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run the notebook

```bash
jupyter notebook notebooks/temperature_control.ipynb
```

---

## 🔍 Explainability with SHAP

**SHAP (SHapley Additive exPlanations)** is applied to see which features matter most to the model.

📊 Example SHAP output:

* **Room temperature** and **outside temperature** → most important
* **Humidity** → smaller effect

---


