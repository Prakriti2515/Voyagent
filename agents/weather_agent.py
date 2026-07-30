import os
import requests

GEOCODE_URL = os.environ["GEOCODE_URL"]
FORECAST_URL = os.environ["FORECAST_URL"]

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail"
}


def get_weather(city_name):
    if city_name.strip() == "":
        return {"error": "Please tell me which city you want the weather for."}

    geocode_response = requests.get(GEOCODE_URL, params={"name": city_name, "count": 1})
    geocode_data = geocode_response.json()

    if "results" not in geocode_data or len(geocode_data["results"]) == 0:
        return {"error": "Sorry, I could not find that place. Please check the spelling."}

    place = geocode_data["results"][0]
    latitude = place["latitude"]
    longitude = place["longitude"]
    place_name = place.get("name", city_name)
    country = place.get("country", "")
    
    forecast_response = requests.get(FORECAST_URL, params={
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    })
    forecast_data = forecast_response.json()

    if "current_weather" not in forecast_data:
        return {"error": "Sorry, weather data is not available right now."}

    current = forecast_data["current_weather"]
    weather_code = current.get("weathercode", -1)
    weather_description = WEATHER_CODES.get(weather_code, "Unknown")

    return {
        "place": place_name + ", " + country,
        "temperature_celsius": current.get("temperature"),
        "windspeed_kmh": current.get("windspeed"),
        "condition": weather_description
    }