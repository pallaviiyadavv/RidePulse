select * from trips;

-- total rides
select count(*) as total_rides from trips ;

-- unique locations in the database
select count(distinct start) as total locations
from trips;

-- avg trip distance
select round(avg(miles) , 2) as avg_miles
from trips;

-- avg trip duration
select round(avg(duration_minutes) , 2 ) as  avg_duration 
from trips;

-- top 10 startting locations
select start , count(*) as ride_count
from trips
group by start
order by ride_count desc
limit 10;

-- hourly demand
select hour_of_day , count(*) as ride_count
from trips
group by hour_of_day
order by hour_of_day;

-- day wise demand
select day_of_week_name , count(*) as ride_count
from trips 
group by day_of_week , day_of_week_name 
order by day_of_week;


-- monthly demand
SELECT
    month,
    COUNT(*) AS ride_count
FROM trips
GROUP BY month
ORDER BY month;

-- categorical distribution
SELECT
    category,
    COUNT(*) AS ride_count
FROM trips
GROUP BY category
ORDER BY ride_count DESC;

-- purpose distribution
SELECT
    purpose,
    COUNT(*) AS ride_count
FROM trips
WHERE purpose IS NOT NULL
GROUP BY purpose
ORDER BY ride_count DESC;

-- top routes
SELECT 
    "start", 
    "end", 
    COUNT(*) AS ride_count 
FROM 
    trips 
-- where "start" != "Unknown Location" and 
-- 	"end" != "Unknown Location"
GROUP BY 
    "start", 
    "end" 
ORDER BY 
    ride_count DESC 
LIMIT 10;


-- Peak vs non-peak
SELECT
    is_peak_hr,
    COUNT(*) AS ride_count
FROM trips
GROUP BY is_peak_hr
ORDER BY is_peak_hr DESC;

-- Weekend vs weekday
SELECT
    is_weekend,
    COUNT(*) AS ride_count
FROM trips
GROUP BY is_weekend;



