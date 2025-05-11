import random
import pandas as pd
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
    
# Load environment variables
load_dotenv()

# Define the API key directly (no need for dotenv if hardcoding)
API_KEY = "5b3ce3597851110001cf62484f716d845905470c9f9ead75d2d6270e"

# List of origin-destination coordinate pairs in Chandigarh
coordinates_list = [
    (30.7415, 76.7794, 30.7221, 76.7417),  # Example coordinates, expand this list
    (30.7522, 76.8008, 30.752, 76.81), 
    (30.765, 76.767, 30.6735, 76.7885),
    # Add more coordinates here...
]

# Weather conditions for data augmentation
weather_conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']

# Function to fetch route data using OpenRouteService API
def fetch_route_data(origin_lat, origin_lon, dest_lat, dest_lon):
    url = f"https://router.hereapi.com/v8/routes?transportMode=car&origin={origin}&destination={destination}&return=summary&apikey={api_key}"

    response = requests.get(url)
    return response.json()

# Function to simulate the dataset
def create_route_entry(route_json, origin_lat, origin_lon, dest_lat, dest_lon):
    if 'routes' in route_json and len(route_json['routes']) > 0:
        route = route_json['routes'][0]
        distance = route['summary']['distance'] / 1000  # Convert meters to kilometers
        duration = route['summary']['duration'] / 60  # Convert seconds to minutes

        # Randomly assign weather, time of day, and day of the week
        weather = random.choice(weather_conditions)
        temperature = round(random.uniform(20, 35), 2)  # Random temperature between 20 and 35°C
        time_of_day = datetime.now().strftime("%H:%M")  # Current time
        day_of_week = datetime.now().strftime("%A")  # Current day of the week
        
        # Generate a unique route id
        route_id = f"[{origin_lat},{origin_lon}]-[{dest_lat},{dest_lon}]-R{random.randint(1, 100)}"
        
        # Return route data
        return {
            "route_id": route_id,
            "source_lat": origin_lat,
            "source_lon": origin_lon,
            "dest_lat": dest_lat,
            "dest_lon": dest_lon,
            "distance_km": distance,
            "duration_min": duration,
            "num_turns": len(route['segments'][0]['steps']),  # Count steps for turns
            "weather": weather,
            "temperature_C": temperature,
            "time_of_day": time_of_day,
            "day_of_week": day_of_week,
            "label": random.choice([0, 1])  # Randomly assign label (0 or 1)
        }
    return None

# Collect data from multiple routes and save it to a CSV
def collect_route_data():
    data = []
    for origin_lat, origin_lon, dest_lat, dest_lon in coordinates_list:
        print(f"Fetching route from ({origin_lat}, {origin_lon}) to ({dest_lat}, {dest_lon})...")
        route_json = fetch_route_data(origin_lat, origin_lon, dest_lat, dest_lon)
        route_entry = create_route_entry(route_json, origin_lat, origin_lon, dest_lat, dest_lon)
        if route_entry:
            data.append(route_entry)
    
    # Save data to CSV file
    df = pd.DataFrame(data)
    df.to_csv('data/routes.csv', index=False)
    print(f"✅ Dataset saved to data/routes.csv")

if __name__ == "__main__":
    collect_route_data()
