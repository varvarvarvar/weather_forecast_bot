# weather_forecast_bot

With this API you can get current weather forecast for different locations all over the world.

# API description

GET request to https://krasavina-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
<br>
<br>
**Parameters**:
<br>
location: input location (required)
<br>
**Returns**:
<br>
Verbal weather description

# Command line usage examples

1.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "Red Square"}' https://krasavina-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"description":"Temperature: 15C, feels like: 13C, overcast.","location":"Red Square"}
```

2.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "Natural History Museum, London"}' https://krasavina-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"description":"Temperature: 25C, feels like: 25C, rain.","location":"Natural History Museum, London"}
```

3.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "Piazza del Colosseo, 1, Roma"}' https://krasavina-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"description":"Temperature: 32C, feels like: 29C, cloudy.","location":"Piazza del Colosseo, 1, Roma"}
```

# Used technology stack

1. [Yandex Weather API](https://yandex.ru/dev/weather/): API with detailed weather info based on latitude and longitude
2. [geopy](https://geopy.readthedocs.io/en/stable/): Python library to convert string address to its latitude and longitude
3. [Flask API](https://flask.palletsprojects.com/en/1.1.x/): RESTful API
4. [Heroku server](https://www.heroku.com/): cloud server platform

# Useful tutorials

1. [Guide to RESTful API with Flask](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
2. [Guide to Deploying a Flask app on Heroku](https://kaushalvivek.github.io/2020-3-30-heroku-flask/)
3. [Yandex Weather API Examples](https://sprut.ai/client/blog/1165)

# TODO

1. More detailed weather description, weather forecast for tomorrow
2. Use async
3. Improve error handling
