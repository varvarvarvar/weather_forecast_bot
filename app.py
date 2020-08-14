from flask import Flask, jsonify, request
import logging

from config import YA_TOKEN
from src import GeoTranslator, MeteoParser, Meteo

app = Flask(__name__)

geo_translator = GeoTranslator()
meteo_parser = MeteoParser(YA_TOKEN)
meteo = Meteo(geo_translator, meteo_parser)


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

    if not response or 'location' not in response:
        error_msg = "Missing required argument 'location'."
        logging.error(error_msg)
        return jsonify(
            {
                'response': None,
                'location': None,
                'error': error_msg
            }
        ), 200

    location = response['location']

    meteo_desc = meteo.forecast(location)

    if 'error' in meteo_desc:
        return jsonify(
            {
                'response': None,
                'location': location,
                'error': meteo_desc['error']
            }
        ), 200

    return jsonify(
        {'response': meteo_desc['response'], 'location': location}
    ), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
