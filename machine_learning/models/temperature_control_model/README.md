# 🌡️ Temperature Control Model

This project builds an **AI model to optimize room temperature**.
It predicts **AC temperature settings, fan speed, and power usage** using past data like weather, occupancy, and room conditions.

The goal: **Save energy ⚡ while keeping rooms comfortable 😌**.

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
│── testing_data.csv # Testing dataset
│── temperature_control.ipynb # Python notebook
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
jupyter notebook temperature_control.ipynb
```

### 4. Run the Simulation

After training and saving the models, you can run the simulation to test predictions on new data.

1. Make sure you have the trained models in your project directory:
   - `best_fan_model.joblib`
   - `best_temp_model.joblib`
   - `best_power_model.joblib`

2. Place your new testing data file in the same directory (for example, `testing_data.csv`).

   > **Note:** In this repository, we provide a sample `testing_data.csv` with 5 rows (generated using Google Gemini) that you can use to test the models.

3. Run the prediction script:

   ```bash
   python run_simulation.py

---

### 🖥️ Sample Output

When you run the script, you should see something like this:

```text
New Fan Speed Predictions {0:high, 1:low, 2:medium, 3:off, 4:on}: [1 2 1 1 2]
New AC Temperature Predictions: [23. 22. 23. 23. 22.]
New Power Consumption Predictions: [1.54924153 1.57909569 1.07031787 1.55151238 1.58543521]
```
This shows the model’s predictions for each of the 5 rows in `testing_data.csv`.

---

## 🔍 Explainability with SHAP

**SHAP (SHapley Additive exPlanations)** is applied to see which features matter most to the model.

📊 Example SHAP output:

* **Room temperature** and **outside temperature** → most important
* **Humidity** → smaller effect

---






