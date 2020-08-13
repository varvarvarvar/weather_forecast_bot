from flask import Flask, jsonify, request

from config import YA_TOKEN
from src import YaWeatherDescriptor

app = Flask(__name__)

descriptor = YaWeatherDescriptor(YA_TOKEN)


@app.route('/')
def index():
    welcome_msg = (
        'This is weather forecast API. <br>'
        'Read the docs here: <br>'
        'https://github.com/varvara-krasavina/weather_forecast_bot#weather_forecast_bot'
    )
    return welcome_msg


@app.route('/weather/api/v1.0/', methods=['GET'])
def forecast():

    response = request.json

    location = response['location']

    weather_desc = descriptor.describe(location)

    if 'error' in weather_desc:
        return jsonify(
            {
                'response': None,
                'location': location,
                'error': weather_desc['error']
            }
        ), 200

    return jsonify(
        {'response': weather_desc['response'], 'location': location}
    ), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
