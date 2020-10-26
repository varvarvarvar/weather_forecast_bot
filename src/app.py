from flask import Flask, jsonify, request
import logging

from .config import YA_TOKEN
from .src import GeoTranslator, MeteoParser, Meteo

from .moesif_monitoring import moesif_settings
from moesifwsgi import MoesifMiddleware

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

geo_translator = GeoTranslator()
meteo_parser = MeteoParser(YA_TOKEN)
meteo = Meteo(geo_translator, meteo_parser)

app.wsgi_app = MoesifMiddleware(app.wsgi_app, moesif_settings)


@app.route('/')
def index():
    welcome_msg = (
        'This is weather forecast API. <br>'
        'Read the docs here: <br>'
        'https://github.com/varvarvarvar/weather_forecast_bot'
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

    logging.info(
        "Location: '%s', response: '%s'" % (location, meteo_desc['response'])
    )
    return jsonify(
        {'response': meteo_desc['response'], 'location': location}
    ), 200
