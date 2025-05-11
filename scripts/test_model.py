import csv
import math

# Haversine formula to calculate distance between two lat/lon pairs
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# Load the dataset
def load_routes(csv_file_path):
    routes = []
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            route = {
                'route_id': row['route_id'],
                'source_lat': float(row['source_lat']),
                'source_lon': float(row['source_lon']),
                'dest_lat': float(row['dest_lat']),
                'dest_lon': float(row['dest_lon']),
                'label': int(row['label'])  # Ideal path indicator
            }
            routes.append(route)
    return routes

# Find the closest route based on coordinates
def find_ideal_route(routes, src_lat, src_lon, dst_lat, dst_lon):
    closest_routes = []

    for route in routes:
        src_dist = haversine(src_lat, src_lon, route['source_lat'], route['source_lon'])
        dst_dist = haversine(dst_lat, dst_lon, route['dest_lat'], route['dest_lon'])
        total_error = src_dist + dst_dist

        closest_routes.append((total_error, route))

    closest_routes.sort(key=lambda x: x[0])
    
    # Filter top matches with same route source-destination and pick the one with label=1
    top_group = [r for e, r in closest_routes if
                 abs(r['source_lat'] - src_lat) < 0.01 and
                 abs(r['source_lon'] - src_lon) < 0.01 and
                 abs(r['dest_lat'] - dst_lat) < 0.01 and
                 abs(r['dest_lon'] - dst_lon) < 0.01]
    
    for r in top_group:
        if r['label'] == 1:
            return r

    return top_group[0] if top_group else None
import folium

def visualize_route(route):
    source = (route['source_lat'], route['source_lon'])
    dest = (route['dest_lat'], route['dest_lon'])

    # Center map around midpoint
    map_center = [(source[0] + dest[0]) / 2, (source[1] + dest[1]) / 2]
    m = folium.Map(location=map_center, zoom_start=13)

    # Add markers
    folium.Marker(source, tooltip="Source", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(dest, tooltip="Destination", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine([source, dest], color='blue', weight=5, opacity=0.7).add_to(m)

    # Draw a line between source and destination
    folium.PolyLine([source, dest], color='blue', weight=5, opacity=0.7).add_to(m)

    # Save or show
    m.save('route_visualization.html')
    print("📍 Route visualization saved to 'route_visualization.html'.")


if __name__ == "__main__":
    # inputs from user
    user_src_lat = float(input("Enter source latitude: "))
    user_src_lon = float(input("Enter source longitude: "))
    user_dst_lat = float(input("Enter destination latitude: "))
    user_dst_lon = float(input("Enter destination longitude: "))

    routes = load_routes("chandigarh_routes.csv")  # raw string

    best_route = find_ideal_route(routes, user_src_lat, user_src_lon, user_dst_lat, user_dst_lon)
    
# After finding the route
if best_route:
    print(f"Ideal Route Found:\nRoute ID: {best_route['route_id']}")
    visualize_route(best_route)
else:
    print("No matching route found.")
    if best_route:
        print(f"Ideal Route Found:\nRoute ID: {best_route['route_id']}")
    else:
        print("No matching route found.")
import folium

def visualize_route(source_lat, source_lon, dest_lat, dest_lon):
    # Ensure coordinates are in (lat, lon) format
    source = (source_lat, source_lon)
    dest = (dest_lat, dest_lon)

    # Center map between the two points
    map_center = [(source[0] + dest[0]) / 2, (source[1] + dest[1]) / 2]
    m = folium.Map(location=map_center, zoom_start=13, tiles="OpenStreetMap")

    # Add source and destination markers
    folium.Marker(source, tooltip="Source", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(dest, tooltip="Destination", icon=folium.Icon(color='red')).add_to(m)

    # Draw the route
    folium.PolyLine([source, dest], color='blue', weight=5, opacity=0.8).add_to(m)

    # Save map
    m.save("route_visualization.html")
    print("✅ Map saved to route_visualization.html")
    # Replace with your actual lat/lon values if hardcoded, or extract from model result
visualize_route(30.7415, 76.7794, 30.7221, 76.7417)
