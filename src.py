import logging
import requests

from geopy.geocoders import Nominatim


class YaWeather:
    """Retrieve weather info from Yandex Weather API.

    """

    def __init__(self, api_token: str) -> None:

        self._api_token = api_token
        self._headers = {'X-Yandex-API-Key': self._api_token}

    def get_weather(self, lat: float, lon: float) -> dict:
        """Send GET request to Yandex Weather API.

        Parameters:
        lat (float): Latitude
        lon (float): Longitude

        Returns:
        dict:Weather information (temperature, wind speed etc)
        See https://yandex.ru/dev/weather/doc/dg/concepts/forecast-info-docpage/#resp-format

        """

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


class YaWeatherDescriptor:
    """Process input location address to form a verbal weather description.

    """

    def __init__(self, ya_api_token: str) -> None:

        self.ya_api = YaWeather(ya_api_token)
        self.geolocator = Nominatim(user_agent='myapplication')

    def form_description(self, weather_data: dict) -> str:
        """Form a verbal weather description based on the weather information.

        Parameters:
        weather_data (dict): Weather information

        Returns:
        str:Verbal weather description

        """

        if 'fact' not in weather_data \
                or 'temp' not in weather_data['fact'] \
                or 'feels_like' not in weather_data['fact'] \
                or 'condition' not in weather_data['fact']:

            logging.error('Incorrect Ya Weather API output')
            return {
                'response': None,
                'error': 'Incorrect Ya Weather API output format.'
            }

        weather_desc = 'Temperature: %sC, feels like: %sC, %s.' % (
            weather_data['fact']['temp'],
            weather_data['fact']['feels_like'],
            weather_data['fact']['condition']
        )

        return {'response': weather_desc}

    def describe(self, input_location: str) -> str:
        """Process input location address to form a verbal weather description.
        Convert input string location address to its respective latitude and longitude.
        Retrieve weather information using the latitude and longitude.
        Form a verbal weather description based on the weather information.

        Parameters:
        input_location (str): Input address

        Returns:
        str:Verbal weather description

        """

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

        # Retrieve weather information using the latitude and longitude.
        weather_data = self.ya_api.get_weather(lat=lat, lon=lon)

        if 'error' in weather_data:
            return weather_data

        # Form a verbal weather description based on the weather information.
        weather_desc = self.form_description(weather_data['response'])

        return weather_desc
