import logging
import requests

from geopy.geocoders import Nominatim


class GeoTranslator:
    """Get latitude and longitude from input location address.

    """

    def __init__(self):

        self.geolocator = Nominatim(user_agent='myapplication')

    def to_coords(self, input_location: str) -> dict:
        """Send input location address to geopy, parse latitude and longitude.

        Parameters:
        input_location (str): Location

        Returns:
        {
        response ((lat: float, lon: float) or None): Latitude and longitude
        error (str, optional): Error description
        }

        """

        location = self.geolocator.geocode(input_location)

        if not location:
            error_msg = "Error parsing location '%s' with geopy." % input_location

            logging.error(error_msg)
            return {
                'response': None,
                'error': error_msg
            }

        lat, lon = location.raw['lat'], location.raw['lon']

        return {'response': (lat, lon)}


class MeteoParser:
    """Form a verbal weather description based on latitude and longitude.

    """

    def __init__(self, api_token: str) -> None:

        self._api_token = api_token
        self._headers = {'X-Yandex-API-Key': self._api_token}

    def _request_data(self, lat: float, lon: float) -> dict:
        """Send GET request to Yandex Weather API.

        Parameters:
        lat (float): Latitude
        lon (float): Longitude

        Returns:
        {
        response (dict or None): Yandex Weather API response
        error (str, optional): Error description
        }
        See https://yandex.ru/dev/weather/doc/dg/concepts/forecast-info-docpage/#resp-format

        """

        base_url = "https://api.weather.yandex.ru/v2/informers?lat=%s&lon=%s" % (
            lat, lon
        )

        try:
            response = requests.get(base_url, headers=self._headers)
            response = response.json()

            if 'status' in response:
                error_msg = 'Error fetching data from Yandex.Weather, %s, %s.' % (
                    response['status'], response['message']
                )
                logging.error(error_msg)
                return {'response': None, 'error': error_msg}

            return {'response': response}

        except Exception as e:
            error_msg = 'Oops! An error occurred: %s.' % e
            logging.error(error_msg)
            return {'response': None, 'error': error_msg}

    def _parse(self, meteo_data: dict) -> dict:
        """Parse Yandex Weather API response to form a verbal weather description.

        Parameters:
        meteo_data (dict): Yandex Weather API response

        Returns:
        {
        response (str or None): Verbal weather description
        error (str, optional): Error description
        }

        """

        if 'fact' not in meteo_data \
                or 'temp' not in meteo_data['fact'] \
                or 'feels_like' not in meteo_data['fact'] \
                or 'condition' not in meteo_data['fact']:

            error_msg = 'Incorrect Ya Weather API output.'
            logging.error(error_msg)
            return {'response': None, 'error': error_msg}

        meteo_desc = 'Temperature: %sC, feels like: %sC, %s.' % (
            meteo_data['fact']['temp'],
            meteo_data['fact']['feels_like'],
            meteo_data['fact']['condition']
        )

        return {'response': meteo_desc}

    def get_data(self, lat: float, lon: float) -> dict:
        """Wrapper for ._request_data and ._parse

        Parameters:
        lat (float): Latitude
        lon (float): Longitude

        Returns:
        {
        response (str or None): Verbal weather description
        error (str, optional): Error description
        }

        """

        meteo_data = self._request_data(lat, lon)
        if 'error' in meteo_data:
            return meteo_data
        meteo_desc = self._parse(meteo_data['response'])

        return meteo_desc


class Meteo:
    """Wrapper for GeoTranslator and MeteoParser.

    """

    def __init__(self, geo_translator, meteo_parser) -> None:
        self.geo_translator = geo_translator
        self.meteo_parser = meteo_parser

    def forecast(self, location: str) -> str:
        """Receive location address as input.
        Get its latitude and longitude.
        Form a verbal weather description based on latitude and longitude.

        Parameters:
        location (str): Location

        Returns:
        {
        response (str or None): Verbal weather description
        error (str, optional): Error description
        }

        """

        coords = self.geo_translator.to_coords(location)

        if 'error' in coords:
            return coords

        lat, lon = coords['response']
        meteo_desc = self.meteo_parser.get_data(lat=lat, lon=lon)

        return meteo_desc
