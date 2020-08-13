from flask import Flask, jsonify, request, abort, make_response

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
    if not response:
        abort(404)

    location = response['location']

    if location not in response:
        abort(404)

    weather_desc = descriptor.describe(location)

    return jsonify(
        {'description': weather_desc, 'location': location}
    ), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Incorrect input format'}), 404)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
