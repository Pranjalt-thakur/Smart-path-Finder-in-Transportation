# Smart Pathfinding in Transportation Systems 🚦🗺️

An intelligent transportation route recommendation system that integrates real-time traffic data, predictive analytics, and user-centric routing to provide efficient, reliable, and sustainable paths for urban commuters.

🚀 Project Overview

Traditional navigation systems often rely solely on shortest-distance or fastest-time algorithms, ignoring factors like live traffic, safety, convenience, or environmental impact.  
This project aims to solve that by building a **smart, adaptable, and intuitive routing platform** using real-time data, automation, and predictive modeling.

🎯 Objectives

- **Achieve Travel Efficiency**: Provide optimal routes based on traffic, road conditions, and user preferences.
- **Real-Time Traffic Management**: Adapt dynamically to current road situations, congestion, and incidents.
- **Environmental Sustainability**: Suggest eco-friendly routes to reduce idle time, fuel consumption, and emissions.
- **Smart Visualization**: Render intuitive route maps for better user decision-making.
- **Automated Data Collection**: Periodically fetch live traffic data using scheduled tasks for accurate model training.

🧠 Features

- Interactive map-based route visualization
- Real-time API integration for traffic, routes, and conditions
- Machine Learning model for travel time prediction
- User inputs for origin & destination
- Automated data logging using cron jobs
- Modular Flask backend

🛠️ Tech Stack

- **Backend**: Python, Flask
- **Visualization**: Folium
- **Data Sources**: HERE Maps API, Google Maps API, OpenRouteService API
- **ML Model**: Random Forest (trained on historical traffic data)
- **Automation**: Cron jobs on Ubuntu
- **Cloud**: (Optional) AWS for scalability and deployment
