import json
import logging

import requests

from config import YA_WEATHER_API, CONDITION_MAPPER


class YaWeather:

    def __init__(self, api_token):
        self._api_token = api_token
        self._headers = {'X-Yandex-API-Key': self._api_token}

    def get_weather(self, lat, lon):

        base_url = "https://api.weather.yandex.ru/v2/forecast?lat=%s&lon=%s" % (lat, lon)

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


class YaWeatherParser:
    def __init__(self):
        pass

    def parse(self, data):
        str = 'Температура %s°C, ощущается как %s°C, %s.' % (
            data['fact']['temp'], data['fact']['feels_like'], CONDITION_MAPPER[data['fact']['condition']]
        )
        return str
