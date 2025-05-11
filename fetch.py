import requests
import datetime

class TrafficData:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def air_index(self):
        """Fetch air quality index (AQI) from OpenAQ API."""
        ENDPOINT = 'https://api.openaq.org/v1/latest'
        parameters = {'coordinates': f'{self.lat},{self.lon}', 'radius': '10000', 'parameter': 'pm25'}
        response = requests.get(ENDPOINT, params=parameters).json()

        if response.get('results'):
            value = response['results'][0]['measurements'][0]['value']
            unit = response['results'][0]['measurements'][0]['unit']
            return f'AQI: {value} {unit}'
        return 'AQI Data Unavailable'

    def is_holiday(self):
        """Check if today is a public holiday using Calendarific API."""
        year = datetime.datetime.now().year
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        ENDPOINT = 'https://calendarific.com/api/v2/holidays'
        parameters = {'api_key': '?api_key=baa9dc110aa712sd3a9fa2a3dwb6c01d4c875950dc32vs', 'country': 'US', 'year': year}
        response = requests.get(ENDPOINT, params=parameters).json()

        holidays = response.get('response', {}).get('holidays', [])
        return any(holiday['date']['iso'] == today for holiday in holidays)

    def is_weekend(self):
        """Check if today is a weekend."""
        return datetime.datetime.now().strftime('%A') in ['Saturday', 'Sunday']

    def weather_data(self):
        """Fetch weather details (temperature, humidity, wind direction) from OpenWeatherMap API."""
        ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'
        parameters = {'lat': self.lat, 'lon': self.lon, 'appid': '0052861c3fc619a0fcb6bf24a07a477e', 'units': 'metric'}
        response = requests.get(ENDPOINT, params=parameters).json()

        temperature = response.get('main', {}).get('temp', 'N/A')
        humidity = response.get('main', {}).get('humidity', 'N/A')
        wind_direction = response.get('wind', {}).get('deg', 'N/A')

        return {
            'temperature': f'Temperature: {temperature}°C',
            'humidity': f'Humidity: {humidity}%',
            'wind_direction': f'Wind Direction: {wind_direction}°'
        }
