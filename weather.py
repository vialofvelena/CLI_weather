import requests
import sys

# Weather condition to emoji mapping
WEATHER_EMOJIS = {
    "clear": "☀️",
    "sunny": "🌞",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "🌥️",
    "mist": "🌫️",
    "patchy rain possible": "🌦️",
    "light rain": "🌧️",
    "moderate rain": "🌧️",
    "heavy rain": "🌧️🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "fog": "🌁",
    "windy": "💨"
}

def get_weather(city):
    """Fetch weather data from wttr.in API."""
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_emoji(condition):
    """Return an emoji based on the weather condition."""
    condition = condition.lower()
    for key in WEATHER_EMOJIS:
        if key in condition:
            return WEATHER_EMOJIS[key]
    return "❓"  # Default if no match found

if len(sys.argv) < 2:
    print("Usage: python weather.py [current|forecast] city [days]")
    sys.exit(1)

command = sys.argv[1]

if command == 'current':
    if len(sys.argv) < 3:
        print("Please provide a city name")
        sys.exit(1)
    
    city = sys.argv[2]
    print(f"Fetching current weather for {city}...")

    weather_data = get_weather(city)
    if weather_data:
        temp_c = weather_data['current_condition'][0]['temp_C']
        condition = weather_data['current_condition'][0]['weatherDesc'][0]['value']
        emoji = get_weather_emoji(condition)
        print(f"🌍 {city}: {temp_c}°C {emoji} ({condition})")
    else:
        print("Error fetching weather")

elif command == 'forecast':
    if len(sys.argv) < 4:
        print("Please provide a city name and number of days")
        sys.exit(1)

    city = sys.argv[2]
    days = int(sys.argv[3])
    print(f"Fetching {days}-day forecast for {city}...")

    weather_data = get_weather(city)
    if weather_data:
        for i in range(days):
            date = weather_data['weather'][i]['date']
            max_temp = weather_data['weather'][i]['maxtempC']
            min_temp = weather_data['weather'][i]['mintempC']
            condition = weather_data['weather'][i]['hourly'][0]['weatherDesc'][0]['value']
            emoji = get_weather_emoji(condition)

            print(f"📅 {date}: {emoji} High: {max_temp}°C, Low: {min_temp}°C ({condition})")
    else:
        print("Error fetching weather")

else:
    print("Command not recognized. Use 'current' or 'forecast'")