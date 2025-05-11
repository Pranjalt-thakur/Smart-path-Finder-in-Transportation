import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os
import pandas as pd
#Hello
df_original = pd.read_csv("chandigarh_routes.csv")

# Function to fetch real-time traffic delay using HERE API
def get_traffic_data(source_lat, source_lon, dest_lat, dest_lon, api_key):
    url = (
        f"https://router.hereapi.com/v8/routes?"
        f"transportMode=car"
        f"&origin={source_lat},{source_lon}"
        f"&destination={dest_lat},{dest_lon}"
        f"&return=summary,travelSummary"
        f"&apikey={api_key}"
    )
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            routes = data.get("routes", [])
            if routes:
                summary = routes[0]["sections"][0].get("summary", {})
                traffic_time = summary.get("duration")
                base_time = summary.get("baseDuration")
                if traffic_time and base_time:
                    return traffic_time - base_time
        print(f"⚠️ No traffic data for route: ({source_lat}, {source_lon}) → ({dest_lat}, {dest_lon})")
    except Exception as e:
        print(f"❌ Error fetching traffic data: {e}")
    return 0

# Load dataset
data = pd.read_csv("chandigarh_routes.csv")
data.fillna(method="ffill", inplace=True)

# Encode categorical columns
label_encoder = LabelEncoder()
data['weather'] = label_encoder.fit_transform(data['weather'])
data['time_of_day'] = label_encoder.fit_transform(data['time_of_day'])
data['day_of_week'] = label_encoder.fit_transform(data['day_of_week'])

# HERE API key
api_key = 'PX2ClkPfcj8NWcLmMbBqb5HTYQg_lNqISfeWQhePLdg'

# Add traffic density if not already present
if 'traffic_density' not in data.columns or data['traffic_density'].isnull().any():
    print("🚗 Fetching traffic data...")
    data['traffic_density'] = data.apply(
        lambda row: get_traffic_data(
            row['source_lat'], row['source_lon'],
            row['dest_lat'], row['dest_lon'], api_key
        ), axis=1
    )
    data.to_csv("chandigarh_routes.csv", index=False)
    print("✅ Traffic data added and saved to 'chandigarh_routes.csv'.")

def categorize_delay(delay):
    if delay < 60:
        return 'low'
    elif delay < 180:
        return 'moderate'
    else:
        return 'high'

data['traffic_level'] = data['traffic_density'].apply(categorize_delay)
data['traffic_level'] = LabelEncoder().fit_transform(data['traffic_level'])

# Features and target
X = data[['source_lat', 'source_lon', 'dest_lat', 'dest_lon', 'distance_km',
          'num_turns', 'weather', 'temperature_C', 'time_of_day', 'day_of_week', 'traffic_level']]
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = model.predict(X_test_scaled)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# Save model
model_path = 'model/random_forest_model_with_traffic.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model training completed and saved to '{model_path}'")
print(data['label'].value_counts())
