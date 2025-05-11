import requests
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

# API keys (hardcoded as requested)
ORS_API_KEY = "5b3ce3597851110001cf62484f716d845905470c9f9ead75d2d6270e"
OWM_API_KEY = "2f63df2fd793cfe70a440660e3494ec1"

# Directory to save dataset
Path("data").mkdir(parents=True, exist_ok=True)

def get_routes(source, destination):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    coordinates = [[source[1], source[0]], [destination[1], destination[0]]]  # [lon, lat]
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": coordinates,
        "alternative_routes": {
            "share_factor": 0.6,
            "target_count": 3
        }
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        print(f"🚨 API error {response.status_code}: {response.text}")
        return []

    data = response.json()
    return data.get('features', [])

def get_weather(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
    res = requests.get(weather_url)

    if res.status_code != 200:
        print(f"⚠️ Weather API error {res.status_code}: {res.text}")
        return "Unknown", 25.0

    data = res.json()
    return data["weather"][0]["main"], data["main"]["temp"]

def extract_route_features(route):
    props = route['properties']['summary']
    geometry = route['geometry']['coordinates']
    return {
        "distance_km": round(props["distance"] / 1000, 2),
        "duration_min": round(props["duration"] / 60, 2),
        "num_turns": len(geometry),
        "elevation_gain": 0
    }

def create_dataset_entry(source, destination):
    routes = get_routes(source, destination)
    weather, temp = get_weather(source[1], source[0])

    entries = []
    durations = []

    for i, route in enumerate(routes):
        features = extract_route_features(route)
        durations.append(features["duration_min"])

        entry = {
            "route_id": f"{source}-{destination}-R{i+1}",
            "source_lat": source[1],
            "source_lon": source[0],
            "dest_lat": destination[1],
            "dest_lon": destination[0],
            "distance_km": features["distance_km"],
            "duration_min": features["duration_min"],
            "num_turns": features["num_turns"],
            "weather": weather,
            "temperature_C": temp,
            "time_of_day": datetime.now().strftime("%H:%M"),
            "day_of_week": datetime.now().strftime("%A"),
        }
        entries.append(entry)

    # Label shortest duration route as optimal
    if durations:
        min_index = durations.index(min(durations))
        for i, e in enumerate(entries):
            e["label"] = 1 if i == min_index else 0

    return entries

def main():
    locations = [
        ((30.7415, 76.7794), (30.7221, 76.7417)),
        ((30.7522, 76.8008), (30.752, 76.81)),
        ((30.765, 76.767), (30.6735, 76.7885)),
        ((30.7282, 76.7841), (30.7448, 76.7875)),
        ((30.7192, 76.7636), (30.7035, 76.8024)),
        ((30.7120, 76.7735), (30.7343, 76.7795)),
        ((30.7419, 76.8168), (30.7375, 76.7684)),
        ((30.7128, 76.8121), (30.7281, 76.7653)),
    ]

    dataset = []

    for src, dest in locations:
        try:
            print(f"Fetching routes from {src} to {dest}...")
            rows = create_dataset_entry(src, dest)
            dataset.extend(rows)
            print(f"✅ Got {len(rows)} route entries")
        except Exception as e:
            print("Error:", e)

    df = pd.DataFrame(dataset)
    df.to_csv("data/routes.csv", index=False)
    print("✅ Dataset saved to data/routes.csv")

if __name__ == "__main__":
    main()
