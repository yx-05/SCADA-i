# 🌡️ Time-to-Cool Model
This project builds an **AI system to optimize room pre-cooling**.
It predicts **how long it will take for a room to reach a target temperature** (e.g., 23°C) using historical HVAC and environmental data.

The goal: **Start pre-cooling at the optimal time ⏱️ to save energy ⚡ while keeping rooms comfortable 😌.**

---

## 💻 Model Training
The model was trained and tested using **ML Pipelines** with **LightGBM**.

### 🔹 1. **Time-to-Cool Prediction (Regression)**
* **Algorithm:** `LGBMRegressor`
* **Task:** Predict the time (in minutes) for the room to reach a target temperature.
* **Method:**

  * Pipeline (`preprocess → regressor`)
  * Train/Validation/Test split: 27280 / 5846 / 5846 rows
  * Censored rows handled separately (30054 censored, 38972 trainable)
  * Scoring metric: **MAE & RMSE**

---

## 🧠 Results

| Metric                     | Value                  |
| -------------------------- | -------------------- |
| Labeled rows               | 75067                |
| Censored rows              | 30054                |
| Trainable rows (non-censored) | 38972             |
| MAE (minutes)              | 0.2638               |
| RMSE                       | 0.2132               |

---

## 📂 Project Files
```
time-to-cool-model/
│── dataset.csv # Input dataset for prediction
│── demo_prediction.py # Simulation of predictions
│── README.md
│── requirements.txt # Necessary package dependencies
│── time_to_cool_model.pkl # Saved model
│── time_to_cool.ipynb # Python notebook with full training pipeline
```

---

## 🚀 How to Use

### 1. Clone the repo

```bash
git clone https://github.com/yx-05/SCADA-i.git
cd SCADA-i/machine_learning/models/time_to_cool_model
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run the notebook

```bash
jupyter notebook time_to_cool.ipynb
```
### 4. Run the demo script
To simulate retrieving data from the database and running predictions, run `demo_prediction.py`. Ensure that your Python environment has all required libraries installed, and that `time_to_cool_model.pkl` and `dataset.csv` are correctly configured with the proper paths.
```bash
python demo_prediction.py
```
---

## 📃 Example output
```bash
Predicted time to reach 23.0°C: 106.6 minutes
```