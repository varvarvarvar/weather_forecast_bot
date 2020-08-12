from flask import Flask, jsonify, request

from config import YA_TOKEN
from src import YaWeather, YaWeatherParser

app = Flask(__name__)

ya_api = YaWeather(YA_TOKEN)
parser = YaWeatherParser()


@app.route('/weather/api/v1.0/', methods=['POST'])
def forecast():

    response = request.json
    lat, lon = float(response['lat']), float(response['lon'])

    weather_data = ya_api.get_weather(lat=lat, lon=lon)
    weather_desc = parser.parse(weather_data)

    return jsonify({'description': weather_desc, 'lat': lat, 'lon': lon}), 201


if __name__ == '__main__':
    app.run(debug=False, port=5000)
