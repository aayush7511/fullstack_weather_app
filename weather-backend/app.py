from urllib.parse import quote_plus

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/weather")
def weather():
    city = request.args.get("city")

    # make sure city is inputted
    if not city or not city.strip():
        return jsonify({"error": "City is required"}), 400

    city = city.strip()

    try:
        # Convert city → lat/long
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote_plus(city)}&count=1"
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return jsonify({"error": "City not found"}), 404

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        # Get weather
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,precipitation,relative_humidity_2m,"
            "wind_speed_10m,wind_gusts_10m,pressure_msl,cloud_cover"
        )

        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "error" in weather_data:
            return jsonify({"error": weather_data.get("reason", "Weather API error")}), 502 
        
        current = weather_data['current']
        if not current:
            return jsonify({"error": "Weather data unavailable"}), 502

        print(current)
        return jsonify({
            "temperature": current['temperature_2m'],
            "wind_speed": current['wind_speed_10m'],
            "precipitation": current['precipitation'],
            "relative_humidity": current['relative_humidity_2m'],
            "wind_gusts": current['wind_gusts_10m'],
            "pressure_msl": current['pressure_msl'],
            "cloud_cover": current['cloud_cover']
        })
    except requests.RequestException as e:
        return jsonify({{"error": "Weather service unavailable"}}), 502
    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)