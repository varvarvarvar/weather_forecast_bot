from flask import Flask, jsonify, request
from config import YA_WEATHER_API, CONDITION_MAPPER
from src import YaWeather, YaWeatherParser

app = Flask(__name__)

api = YaWeather(YA_WEATHER_API)
parser = YaWeatherParser()


@app.route('/weather/api/v1.0/', methods=['POST'])
def get_forecast():

    lat, lon = float(request.json['lat']), float(request.json['lon'])

    data = api.get_weather(lat=lat, lon=lon)
    str = parser.parse(data)

    return jsonify({'temp': str, 'lat': request.json['lat'], 'lon': request.json['lon']}), 201


if __name__ == '__main__':
    app.run(debug=False)
