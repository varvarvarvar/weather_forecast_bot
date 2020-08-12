import logging
import requests


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
    def __init__(self):
        pass

    def describe(self, weather_data):
        weather_desc = 'Temperature: %sC, feels like: %sC, %s.' % (
            weather_data['fact']['temp'], weather_data['fact']['feels_like'],
            weather_data['fact']['condition']
        )
        return weather_desc
