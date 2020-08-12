from flask import Flask, jsonify, request

from geopy.geocoders import Nominatim

from config import YA_TOKEN
from src import YaWeather, YaWeatherParser

app = Flask(__name__)

ya_api = YaWeather(YA_TOKEN)
parser = YaWeatherParser()

geolocator = Nominatim(user_agent='myapplication')


@app.route('/weather/api/v1.0/', methods=['GET'])
def forecast():

    response = request.json
    location = response['location']

    location = geolocator.geocode(location)
    lat, lon = location.raw['lat'], location.raw['lon']

    weather_data = ya_api.get_weather(lat=lat, lon=lon)
    weather_desc = parser.parse(weather_data)

    return jsonify({'description': weather_desc, 'lat': lat, 'lon': lon}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
