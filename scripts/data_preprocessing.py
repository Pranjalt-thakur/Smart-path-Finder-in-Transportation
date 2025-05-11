import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
import numpy as np

df = pd.read_csv("data/routes.csv")

# Fill numerical columns
for col in ['source_lat', 'source_lon', 'dest_lat', 'dest_lon',
            'distance_km', 'duration_min', 'num_turns',
            'temperature_C', 'traffic_density']:
    if df[col].isnull().any():
        df[col].fillna(np.random.uniform(df[col].min(), df[col].max()), inplace=True)

# Fill categorical columns
for col in ['weather', 'time_of_day', 'day_of_week', 'label']:
    if df[col].isnull().any():
        df[col].fillna(np.random.choice(df[col].dropna().unique()), inplace=True)

df.to_csv("chandigarh_routes.csv", index=False)

data = pd.read_csv("chandigarh_routes.csv")

data.fillna(method="ffill", inplace=True)

label_encoder = LabelEncoder()

data['weather'] = label_encoder.fit_transform(data['weather'])
data['time_of_day'] = label_encoder.fit_transform(data['time_of_day'])
data['day_of_week'] = label_encoder.fit_transform(data['day_of_week'])

# Separate features (X) and label (y)
X = data[['source_lat', 'source_lon', 'dest_lat', 'dest_lon', 'distance_km', 'num_turns', 'weather', 'temperature_C', 'time_of_day', 'day_of_week']]
y = data['label']  # Assuming 'label' is the target (0 = bad, 1 = good route)

# Train-Test Split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling (Normalize features for better model performance)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Data Preprocessing Completed")
