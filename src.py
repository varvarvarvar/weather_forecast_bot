import logging
import requests

from geopy.geocoders import Nominatim


class YaWeather:

    def __init__(self, api_token):
        self._api_token = api_token
        self._headers = {'X-Yandex-API-Key': self._api_token}

    def get_weather(self, lat, lon):

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
                return None

            return response

        except Exception as e:
            logging.error('Oops! En error occurred: %s' % e)

        return None


class YaWeatherDescriptor:
    def __init__(self, ya_api_token):

        self.ya_api = YaWeather(ya_api_token)
        self.geolocator = Nominatim(user_agent='myapplication')

    def form_description(self, weather_data):

        if 'fact' not in weather_data \
                or 'temp' not in weather_data['fact'] \
                or 'feels_like' not in weather_data['fact'] \
                or 'condition' not in weather_data['fact']:
            return None

        weather_desc = 'Temperature: %sC, feels like: %sC, %s.' % (
            weather_data['fact']['temp'],
            weather_data['fact']['feels_like'],
            weather_data['fact']['condition']
        )
        return weather_desc

    def describe(self, input_location):

        location = self.geolocator.geocode(input_location)

        if not location:
            return "Can't parse this location."

        lat, lon = location.raw['lat'], location.raw['lon']

        weather_data = self.ya_api.get_weather(lat=lat, lon=lon)

        if not weather_data:
            return 'Internal error.'

        weather_desc = self.form_description(weather_data)

        if not weather_desc:
            return 'Internal error.'

        return weather_desc
