## 📁 Files
`EDA.ipynb` → An comprehensive overview of the synthetic dataset with visualization and analysis

`dataset.csv` → The synthetic dataset contain time series data with sensor data, occupancy status and air conditioner control. 

`descriptio.csv` → A file explaining each column of the `dataset.csv`

`synthesize.py` → A python script to synthesize the `dataset.csv`

## 📊 Dataset

* **105k+ rows** of synthetic data with numerical and categorical data
* Example row:

| Timestamp | Hour of day | Day of week | Day of year | Outside temp | Outside humidity | Weather condition | Occupany count | Is occupied | Room temp | Power kw | Fan speed | AC temp setting | AC control reason |  
| ---- | ------------ | -------- | --------- | --------- | --------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 2024-01-01  13:20:00    |   13   | 0    | 1       | 31.540126254344397   | 94.39886728711471  |cloudy |13.0 |1| 23.644217546112497    | 1.6|medium  | 22°C   | ACTION: Normal cooling (warm)   |

---
