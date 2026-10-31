import requests

def get_weather(location: str = "Nairobi") -> str:
    """
    Get current weather and short forecast for a location in Kenya.
    Uses free Open-Meteo API (no API key needed).
    """
    # Simple mapping for common Kenyan locations (you can expand later)
    locations = {
        "nairobi": (1.2921, 36.8219),
        "nakuru": (-0.3031, 36.0800),
        "kisumu": (-0.0917, 34.7680),
        "mombasa": (-4.0435, 39.6682),
        "eldoret": (0.5143, 35.2698),
        "thika": (-1.0333, 37.0693),
        "nyeri": (-0.4201, 36.9476),
    }

    loc = location.lower().strip()
    if loc in locations:
        lat, lon = locations[loc]
    else:
        # Default to Nairobi if location not found
        lat, lon = 1.2921, 36.8219
        location = "Nairobi (default)"

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Africa/Nairobi",
        "forecast_days": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        current = data.get("current", {})
        daily = data.get("daily", {})

        result = f"""
Weather for {location.title()}:

Current:
- Temperature: {current.get('temperature_2m')}°C
- Humidity: {current.get('relative_humidity_2m')}%
- Rain: {current.get('precipitation')} mm
- Wind: {current.get('wind_speed_10m')} km/h

Next 3 days:
"""
        for i in range(min(3, len(daily.get("time", [])))):
            result += f"- {daily['time'][i]}: {daily['temperature_2m_min'][i]}°C to {daily['temperature_2m_max'][i]}°C | Rain: {daily['precipitation_sum'][i]} mm\n"

        return result.strip()

    except Exception as e:
        return f"Sorry, I could not get the weather right now. Error: {str(e)}"