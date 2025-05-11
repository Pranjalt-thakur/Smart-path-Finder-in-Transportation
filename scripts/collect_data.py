import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define parameters
num_routes = 700
start_date = datetime(2025, 4, 20)  # Starting approximately 17 days ago

# Create base coordinates around Chandigarh (from the original dataset)
# Create a pool of coordinates based on the range in the original dataset
lat_min, lat_max = 30.67, 30.78
lon_min, lon_max = 76.70, 76.85

# Weather conditions that appear in the original dataset
weather_conditions = ["Clear", "Clouds", "Rain", "Fog"]
weather_weights = [0.25, 0.35, 0.25, 0.15]  # Adjust based on original data distribution

# Times of day that appear in the original dataset
times_of_day = ["08:00", "10:03", "12:30", "15:45", "18:20", "21:10"]

# Days of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Generate route pairs
def generate_route_pairs(num_unique_pairs):
    route_pairs = []
    for _ in range(num_unique_pairs):
        # Generate source coordinates
        source_lat = round(random.uniform(lat_min, lat_max), 6)
        source_lon = round(random.uniform(lon_min, lon_max), 6)
        
        # Generate destination coordinates (ensuring they're different from source)
        dest_lat = round(random.uniform(lat_min, lat_max), 6)
        dest_lon = round(random.uniform(lon_min, lon_max), 6)
        
        # Ensure source and destination are not too close
        while math.sqrt((source_lat - dest_lat)**2 + (source_lon - dest_lon)**2) < 0.01:
            dest_lat = round(random.uniform(lat_min, lat_max), 6)
            dest_lon = round(random.uniform(lon_min, lon_max), 6)
        
        route_pairs.append((source_lat, source_lon, dest_lat, dest_lon))
    
    return route_pairs

# We'll create about 200 unique route pairs, with 1-3 variations each to get to 500 routes
route_pairs = generate_route_pairs(300)

# Prepare the data list
data = []
current_date = start_date
route_count = 0
day_count = 0
routes_per_day = 30

# For each unique route pair
for pair_idx, (source_lat, source_lon, dest_lat, dest_lon) in enumerate(route_pairs):
    # Decide how many variations of this route (1-3)
    variations = random.randint(1, 3)
    
    # For each variation of this route
    for var in range(1, variations + 1):
        # Set the date/time
        if route_count % routes_per_day == 0 and route_count > 0:
            day_count += 1
            current_date = start_date + timedelta(days=day_count)
        
        # Get day of week
        day_of_week = days_of_week[current_date.weekday()]
        
        # Time of day - select sequential times to make it look realistic
        time_index = (route_count // 5) % len(times_of_day)
        time_of_day = times_of_day[time_index]
        
        # Generate route metrics
        distance_km = round(random.uniform(1.0, 8.0), 2)
        duration_min = round(distance_km * (1.5 + random.uniform(0.2, 0.8)), 2)
        num_turns = random.randint(10, 120)
        weather = random.choices(weather_conditions, weights=weather_weights)[0]
        temperature_C = round(random.uniform(18.0, 36.0), 2)
        traffic_density = random.randint(1, 100)
        
        # Label - make R1 routes more likely to be labeled 1
        if var == 1:
            label = 1 if random.random() < 0.7 else 0
        else:
            label = 1 if random.random() < 0.1 else 0
            
        # Create route ID
        route_id = f"({source_lat}, {source_lon})-({dest_lat}, {dest_lon})-R{var}"
        
        # Add to data
        data.append({
            "route_id": route_id,
            "source_lat": source_lon,  # These appear swapped in the original data
            "source_lon": source_lat,  # These appear swapped in the original data
            "dest_lat": dest_lon,      # These appear swapped in the original data
            "dest_lon": dest_lat,      # These appear swapped in the original data
            "distance_km": distance_km,
            "duration_min": duration_min,
            "num_turns": num_turns,
            "weather": weather,
            "temperature_C": temperature_C,
            "time_of_day": time_of_day,
            "day_of_week": day_of_week,
            "label": label,
            "traffic_density": traffic_density
        })
        
        route_count += 1
        if route_count >= num_routes:
            break
    
    if route_count >= num_routes:
        break

# Create DataFrame
df = pd.DataFrame(data)

# Write to CSV - not actually writing the file but showing the output
df.to_csv("chandigarh_routes.csv", index=False)
