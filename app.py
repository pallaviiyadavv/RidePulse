from flask import Flask, render_template, request
import pandas as pd
import joblib
from sqlalchemy import create_engine

app = Flask(__name__)

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:pallavi@localhost:5432/ridepulse"
)

# Load your pre-saved machine learning model
# Make sure you saved your model earlier using: joblib.dump(model, 'model.pkl')

model_package  = joblib.load('ride_demand_model.pkl')
model = model_package["model"] 
low_threshold = model_package["low_threshold"]
high_threshold = model_package["high_threshold"]
locations = sorted(
    model
    .named_steps["preprocessor"]
    .named_transformers_["location"]
    .categories_[0]
)

@app.route('/')
def home():
    # Render the input HTML form page
    return render_template('index.html' , locations = locations)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Model not found on server.", 500

    # 1. Grab inputs from the HTML Form
    start = request.form["start"]
    time = request.form["time"]
    hour = int(time.split(":")[0])

    # 3. Pack data exactly matching the columns your model was trained on

    # create input in the same format as used during training
    input_data = pd.DataFrame({
        "start" : [start] , 
        "hour_of_day" : [hour]
    })
    
    # NOT REQUIRED FOR CURRENT MODEL SINCE IT ONLY WORKS WITH TWO FEATURES
    # HOUR AND START LOCATION
    # Re-create the One-Hot Encoded variables for the category
    # # If the user selected 'Business', Business=1 and Personal=0 (and vice versa)
    # business = 1 if category == 'Business' else 0
    # personal = 1 if category == 'Personal' else 0


    # 4. Generate the numerical demand prediction
    raw_prediction = model.predict(input_data)[0]

    # 5. Categorize the prediction into LOW/MEDIUM/HIGH demand tiers
    if raw_prediction <= low_threshold:
        demand_status = "LOW"
        color_class = "text-success"   # Green text
    elif raw_prediction <= high_threshold:
        demand_status = "MEDIUM"
        color_class = "text-warning"  # Yellow/Orange text
    else:
        demand_status = "HIGH"
        color_class = "text-danger"   # Red text

    # 6. Send the categorized tier back to the HTML result page
    return render_template('result.html', 
                           status=demand_status, 
                           raw_prediction=round(raw_prediction, 2),
                           start = start,
                           time = time , 
                           locations = locations, #yaha location firse bheja kyuki eske predicio bdd imdrx wala page render hoga or uske liye locations toh chiye hai
                           color=color_class)

@app.route('/dashboard')
def dashboard():
    total_rides = pd.read_sql("select count(*) as total_rides from trips", engine).iloc[0]["total_rides"]

    total_locations = pd.read_sql("select count(distinct start) as total_locations from trips", engine).iloc[0]["total_locations"]

    avg_miles = pd.read_sql("select avg(miles) as avg_miles from trips", engine).iloc[0]["avg_miles"]

    avg_duration = pd.read_sql("select avg(duration_minutes) as avg_duration     from trips", engine).iloc[0]["avg_duration"]

    hourly_data = pd.read_sql('''-- hourly demand
                    select hour_of_day , count(*) as ride_count
                    from trips
                    group by hour_of_day
                    order by hour_of_day''' , engine)

    hours = hourly_data["hour_of_day"].tolist()
    ride_counts = hourly_data["ride_count"].tolist()

    day_data = pd.read_sql('''-- daily demand
                        select day_of_week_name , count(*) as ride_count
                        from trips 
                        group by day_of_week , day_of_week_name 
                        order by day_of_week
                    ''' , engine)
    days = day_data["day_of_week_name"].tolist()
    day_counts = day_data["ride_count"].tolist()#say_count=[1,2,....]

    # Top start locations
    location_data = pd.read_sql(
    """
    SELECT "start" as start_location, COUNT(*) AS ride_count
    FROM trips
    GROUP BY "start"
    ORDER BY ride_count DESC
    LIMIT 10
    """,
    engine
    )

    top_locations = location_data["start_location"].tolist()
    location_counts = location_data["ride_count"].tolist()

    return render_template(
                        'dashboard.html',
                        total_rides=total_rides,
                        total_locations=total_locations,
                        avg_miles=round(avg_miles, 2),
                        avg_duration=round(avg_duration, 2),
                        hours=hours,
                        ride_counts=ride_counts,         
                        days=days,
                        day_counts=day_counts,
                        top_locations=top_locations,
                        location_counts=location_counts)
                    


if __name__ == '__main__':
    app.run(debug=True)
