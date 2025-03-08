import requests
import sys


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


WEATHER_FORTUNES = {
    "sunny": "🌞 A bright day brings bright opportunities!",
    "rain": "🌧️ Some clouds may darken the sky, but opporunities can shine through!",
    "cloudy": "☁️ Unclear skies may mean surprises ahead... stay open to new paths!",
    "snow": "❄️ A peaceful day for reflection and relaxation. Stay warm and cozy!",
    "storm": "⛈️ There may be lightning and thunder, but wait for the storm to pass!",
    "fog": "🌫️ Things might seem unclear now, but the path will reveal itself soon.",
    "windy": "💨 Winds of change are coming... embrace the journey!"
}

def get_weather(city):
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_emoji(condition):
    condition = condition.lower()
    for key in WEATHER_EMOJIS:
        if key in condition:
            return WEATHER_EMOJIS[key]
    return "❓"

def get_weather_fortune(condition):
    condition = condition.lower()
    if "sunny" in condition or "clear" in condition:
        return WEATHER_FORTUNES["sunny"]
    elif "rain" in condition:
        return WEATHER_FORTUNES["rain"]
    elif "cloudy" in condition or "overcast" in condition:
        return WEATHER_FORTUNES["cloudy"]
    elif "snow" in condition:
        return WEATHER_FORTUNES["snow"]
    elif "storm" in condition or "thunder" in condition:
        return WEATHER_FORTUNES["storm"]
    elif "fog" in condition or "mist" in condition:
        return WEATHER_FORTUNES["fog"]
    elif "windy" in condition:
        return WEATHER_FORTUNES["windy"]
    else:
        return "🔮 The future is uncertain. Keep an open mind!"

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
        temp_f = weather_data['current_condition'][0]['temp_F']
        feels_like_c = weather_data['current_condition'][0]['FeelsLikeC']
        feels_like_f = weather_data['current_condition'][0]['FeelsLikeF']
        condition = weather_data['current_condition'][0]['weatherDesc'][0]['value']
        emoji = get_weather_emoji(condition)
        fortune = get_weather_fortune(condition)

        print(f"\n🌍 {city}: {temp_c}°C / {temp_f}°F {emoji} ({condition})")
        print(f"🤔 Feels Like: {feels_like_c}°C / {feels_like_f}°F")

        if "alerts" in weather_data and weather_data["alerts"]:
            print("\n🚨 WEATHER ALERTS:")
            for alert in weather_data["alerts"]:
                print(f"⚠️ {alert['headline']}: {alert['desc']}")
        else:
            print("\n✅ No active weather alerts.")

    
        print(f"\n🔮 Fortune: {fortune}")

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
            max_temp_c = weather_data['weather'][i]['maxtempC']
            min_temp_c = weather_data['weather'][i]['mintempC']
            max_temp_f = weather_data['weather'][i]['maxtempF']
            min_temp_f = weather_data['weather'][i]['mintempF']
            condition = weather_data['weather'][i]['hourly'][0]['weatherDesc'][0]['value']
            emoji = get_weather_emoji(condition)
            fortune = get_weather_fortune(condition)

            print(f"\n📅 {date}: {emoji} High: {max_temp_c}°C / {max_temp_f}°F, Low: {min_temp_c}°C / {min_temp_f}°F ({condition})")
            print(f"🔮 Fortune: {fortune}")
    else:
        print("Error fetching weather")

else:
    print("Command not recognized. Use 'current' or 'forecast'")