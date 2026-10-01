## 🚕 RidePulse

RidePulse is a ride demand analytics and prediction web app built using historical ride data.

I built this project to understand the complete flow of a data science project  from cleaning raw data and finding patterns to training a machine learning model and putting it into a Flask application.

The app lets a user select a **starting location and time** and gives an estimate of the historical ride demand for that location and hour.

It also has a dashboard that shows overall ride patterns using data stored in PostgreSQL.

> RidePulse works with historical ride data, so the prediction represents historical demand patterns and not real-time driver availability.

---

## What I Built

The project has two main parts:

### 1. Demand Prediction

A user selects:

- Starting location
- Time

The selected time is converted into an hour, and the trained model predicts the expected number of historically recorded rides.

The prediction is then shown as:

**LOW / MEDIUM / HIGH**

### 2. Analytics Dashboard

The dashboard gives an overview of the dataset through:

- Total rides
- Number of locations
- Average trip distance
- Average trip duration
- Hourly ride demand
- Demand by day
- Top 10 starting locations

---

## How I Built It

The project started with a raw ride dataset containing information such as:

START_DATE
END_DATE
CATEGORY
START
STOP
MILES
PURPOSE


### Step 1 :  Data Cleaning

I cleaned the raw data and converted the date columns into useful formats. I also created the following features:

- `duration_minutes`
- `month`
- `day`
- `hour_of_day`
- `day_of_week`
- `day_of_week_name`
- `is_peak_hr`
- `is_weekend`

The cleaned data was saved as `cleaned_data.csv`.

### Step 2 : Exploratory Data Analysis

Before building the model, I explored the data to understand how rides were distributed. The analysis included:

- Hourly ride demand
- Daily ride demand
- Top starting locations
- Top routes
- Monthly patterns
- Average distance and duration
- Distance vs duration
- Day × hour demand patterns

This helped me understand which factors were useful for defining ride demand.

### Step 3 : Defining Demand

The original dataset contains individual trips, so I needed to create a demand value that the model could predict.

I grouped the trips by:

```
starting location + hour of day
```

and counted the number of rides.

For example:

```
Cary | 18 | 5
```

means that 5 recorded rides started from Cary during hour 18.

> **Historical demand** = number of recorded rides from a starting location during a particular hour.

### Step 4 : Machine Learning

For the first version, I experimented with different ways of constructing the demand dataset. The final model uses:

- `start`
- `hour_of_day`

Since `start` is categorical data, I used `OneHotEncoder` to encode the locations. The encoded data is then passed to a **Random Forest Regressor**. The complete preprocessing and model are kept inside a Scikit-learn `Pipeline`.

```
Starting Location
       ↓
OneHotEncoder
       ↓
Random Forest
       ↓
Predicted Demand
```

### Step 5 — Model Evaluation

| Metric | Value |
| ------ | ----- |
| MAE    | 0.539 |
| RMSE   | 1.052 |
| R²     | 0.348 |

The model is an MVP rather than a production forecasting system. The dataset is relatively small and many location-hour combinations have very few rides, which makes the prediction problem sparse.

### Step 6 : Connecting the Model to Flask

After training, I saved the model using `joblib`. Instead of training the model every time the application starts, Flask loads the saved model and uses it for predictions.

The prediction flow is:

```
User selects location + time
             ↓
        Flask receives input
             ↓
       Extracts the hour
             ↓
       Saved ML model
             ↓
     Predicted ride demand
             ↓
        LOW / MEDIUM / HIGH
             ↓
         Result page
```

### Step 7 : PostgreSQL & SQL

I also stored the cleaned ride data in PostgreSQL. The database contains a `trips` table with the cleaned trip information and engineered features.

I used SQL queries to calculate:

- Total rides
- Unique locations
- Average distance
- Average duration
- Hourly demand
- Daily demand
- Top starting locations

These results are then sent from Flask to the dashboard.

### Step 8 : Dashboard

The dashboard is built using Flask, Jinja2 and Chart.js. It currently contains three main visualizations:

- **Hourly Ride Demand** — shows how ride activity changes throughout the day.
- **Demand by Day** — shows the number of recorded rides for each day of the week.
- **Top 10 Start Locations** — shows the locations with the highest recorded ride activity.

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- PostgreSQL
- SQL
- SQLAlchemy
- Flask
- Jinja2
- Chart.js
- HTML/CSS
- Joblib

---

## Project Structure

```
RidePulse/
│
├── database/
│   ├── load_data.py
│   └── queries.sql
│
├── datasets/
│   ├── Dataset.csv
│   └── cleaned_data.csv
│
├── ML Model/
│   └── ride_demand_model.pkl
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── dashboard.html
│
├── app.py
├── data_cleaning.ipynb
├── eda.ipynb
├── model_train.ipynb
└── README.md
```

---

## Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd RidePulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Create a database named:

```
ridepulse
```

Then update the PostgreSQL connection details in:

- `app.py`
- `database/load_data.py`

### 5. Load the data

```bash
cd database
python load_data.py
```

### 6. Run Flask

Go back to the project root and run:

```bash
python app.py
```

Then open: <http://127.0.0.1:5000/>

---

## Limitations

This project is based on historical trip records, so it does not know:

- Current driver availability
- Live ride requests
- Traffic conditions
- Real-time events
- Weather conditions

The current prediction also uses only starting location and hour of day. A larger dataset and additional real-world features could make the demand prediction more useful.

---

## What I Learned

While building RidePulse, I worked through the complete process of taking a dataset and turning it into a working application:

```
Raw Data
   ↓
Cleaning
   ↓
EDA
   ↓
Feature Engineering
   ↓
Demand Definition
   ↓
Machine Learning
   ↓
Model Evaluation
   ↓
Flask
   ↓
PostgreSQL + SQL
   ↓
Dashboard
```

The main thing I wanted to learn from this project was not just how to train a model, but how the different parts of a data project connect together to form an actual application.
