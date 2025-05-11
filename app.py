from flask import Flask, render_template, request
import folium
from folium.plugins import HeatMap
import requests
import datetime
import openrouteservice

# app and API keys
app = Flask(__name__, template_folder='template')

HERE_API_KEY = "PX2ClkPfcj8NWcLmMbBqb5HTYQg_lNqISfeWQhePLdg"
ORS_API_KEY = "5b3ce3597851110001cf62484f716d845905470c9f9ead75d2d6270e"

def geocode_location(location_name, api_key):
    """Convert location name to (lat, lng) using OpenRouteService."""
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        'api_key': api_key,
        'text': location_name,
        'size': 1
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['features']:
        coords = data['features'][0]['geometry']['coordinates']
        return coords[1], coords[0]  # (lat, lng)
    else:
        raise ValueError(f"Location not found: {location_name}")

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

# def predict_traffic(...):  # Left as a stub
#     return {}

@app.route('/', methods=['GET', 'POST'])
def get_map():
    formatted_duration = ""
    traffic_prediction = ""
    start_location = end_location = vehicle_type = ""
    lat1 = lng1 = lat2 = lng2 = ""

    # Default map centered at Waknaghat
    default_lat, default_lng = 30.9672, 77.0996
    m = folium.Map(location=[default_lat, default_lng], zoom_start=14)
    map_html = m._repr_html_()

    if request.method == 'POST':
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        vehicle_type = request.form['vehicle_type']

        try:
            lat1, lng1 = geocode_location(start_location, ORS_API_KEY)
            lat2, lng2 = geocode_location(end_location, ORS_API_KEY)
        except ValueError as e:
            return render_template(
                'index.html',
                map_html=map_html,
                duration="",
                traffic_prediction=str(e),
                start_location=start_location,
                end_location=end_location,
                vehicle_type=vehicle_type
            )

        # HERE API: travel duration
        here_url = f"https://router.hereapi.com/v8/routes?transportMode={vehicle_type}&origin={lat1},{lng1}&destination={lat2},{lng2}&return=travelSummary&apikey={HERE_API_KEY}"
        here_response = requests.get(here_url).json()

        if 'routes' in here_response and here_response['routes']:
            travel_time_sec = here_response['routes'][0]['sections'][0]['travelSummary']['duration']
            formatted_duration = format_duration(travel_time_sec)

        # Traffic Heatmap
        traffic_url = f"https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=bbox:{lng1},{lat1},{lng2},{lat2}&apiKey={HERE_API_KEY}"
        traffic_response = requests.get(traffic_url).json()

        heatmap_coords = []
        for result in traffic_response.get('results', []):
            for link in result.get('location', {}).get('shape', {}).get('links', []):
                for point in link.get('points', []):
                    heatmap_coords.append((point['lat'], point['lng']))

        # Map setup
        m = folium.Map(location=[(lat1 + lat2) / 2, (lng1 + lng2) / 2], zoom_start=14)
        if heatmap_coords:
            HeatMap(heatmap_coords).add_to(m)
            #   HeatMap(heatmap_coords, radius=10, blur=15, min_opacity=0.2, max_zoom=14).add_to(m)

        # Route with OpenRouteService
        ors_client = openrouteservice.Client(key=ORS_API_KEY)
        coords = [[lng1, lat1], [lng2, lat2]]

        profile = {
            'car': 'driving-car',
            'bicycle': 'cycling-regular',
            'pedestrian': 'foot-walking'
        }.get(vehicle_type, 'driving-car')

        route = ors_client.directions(coordinates=coords, profile=profile, format='geojson')
        route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]
        folium.PolyLine(route_coords, color="blue", weight=3, opacity=0.8).add_to(m)

        folium.Marker([lat1, lng1], popup='Start', icon=folium.Icon(color='green')).add_to(m)
        folium.Marker([lat2, lng2], popup='End', icon=folium.Icon(color='red')).add_to(m)

        map_html = m._repr_html_()

    return render_template(
        'index.html',
        map_html=map_html,
        duration=formatted_duration,
        traffic_prediction=traffic_prediction,
        start_location=start_location,
        end_location=end_location,
        vehicle_type=vehicle_type
    )

if __name__ == '__main__':
    app.run(debug=True)