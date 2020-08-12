from flask import Flask, jsonify, request

from geopy.geocoders import Nominatim

from config import YA_TOKEN
from src import YaWeather, YaWeatherDescriptor

app = Flask(__name__)

ya_api = YaWeather(YA_TOKEN)
descriptor = YaWeatherDescriptor()

geolocator = Nominatim(user_agent='myapplication')


@app.route('/weather/api/v1.0/', methods=['GET'])
def forecast():

    response = request.json
    input_location = response['location']

    location = geolocator.geocode(input_location)
    if not location:
        weather_desc = "I'm sorry but I couldn't parse this location."
    else:
        lat, lon = location.raw['lat'], location.raw['lon']

        weather_data = ya_api.get_weather(lat=lat, lon=lon)
        weather_desc = descriptor.describe(weather_data)

    return jsonify(
        {'description': weather_desc, 'location': input_location}
    ), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
