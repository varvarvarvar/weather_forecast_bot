import logging
import requests

from geopy.geocoders import Nominatim


class GeoTranslator:

    def __init__(self):

        self.geolocator = Nominatim(user_agent='myapplication')

    def to_coords(self, input_location: str) -> dict:

        # Convert input string location to its respective latitude and longitude.
        location = self.geolocator.geocode(input_location)

        if not location:
            logging.error(
                "Geopy couldn't parse this location."
            )
            return {
                'response': None,
                'error': "Geopy couldn't parse this location."
            }

        lat, lon = location.raw['lat'], location.raw['lon']

        return {'response': (lat, lon)}


class MeteoParser:

    def __init__(self, api_token: str) -> None:

        self._api_token = api_token
        self._headers = {'X-Yandex-API-Key': self._api_token}

    def _request_data(self, lat: float, lon: float) -> dict:

        base_url = "https://api.weather.yandex.ru/v2/forecast?lat=%s&lon=%s" % (
            lat, lon
        )

        try:
            response = requests.get(base_url, headers=self._headers)
            response = response.json()

            if 'status' in response:
                logging.error(
                    'Error fetching data from Yandex.Weather, %s, %s',
                    response['status'], response['message']
                )
                return {'response': None, 'error': response['message']}

            return {'response': response}

        except Exception as e:
            logging.error('Oops! En error occurred: %s' % e)
            return {'response': None, 'error': e}

    def _parse(self, weather_data: dict) -> dict:

        if 'fact' not in weather_data \
                or 'temp' not in weather_data['fact'] \
                or 'feels_like' not in weather_data['fact'] \
                or 'condition' not in weather_data['fact']:

            logging.error('Incorrect Ya Weather API output')

            return {
                'response': None,
                'error': 'Incorrect Ya Weather API output format.'
            }

        weather_desc = {
            'temp': weather_data['fact']['temp'],
            'feels_like': weather_data['fact']['feels_like'],
            'condition': weather_data['fact']['condition']
        }

        return {'response': weather_desc}

    def get_data(self, lat: float, lon: float) -> dict:

        weather_data = self._request_data(lat, lon)
        if 'error' in weather_data:
            return weather_data
        weather_data = self._parse(weather_data['response'])

        return weather_data


class Meteo:

    def __init__(self, geo_translator, meteo_parser) -> None:
        self.geo_translator = geo_translator
        self.meteo_parser = meteo_parser

    def forecast(self, input_location: str) -> str:

        response = self.geo_translator.to_coords(input_location)

        if 'error' in response:
            return response
        lat, lon = response['response']

        # Retrieve weather information using the latitude and longitude.
        weather_data = self.meteo_parser.get_data(lat=lat, lon=lon)

        if 'error' in weather_data:
            return weather_data

        # Form a verbal weather description based on the weather information.
        weather_desc = 'Temperature: %sC, feels like: %sC, %s.' % (
            weather_data['response']['temp'],
            weather_data['response']['feels_like'],
            weather_data['response']['condition']
        )

        return {'response': weather_desc}
