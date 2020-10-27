# weather_forecast_bot

With this API you can get current weather forecast for different locations all over the world.

# API description

GET request to https://varvara-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
<br>
<br>
**Parameters:**
```
location (str): Location
```
**Returns:**
```
{
location (str or None): Location
response (str or None): Verbal weather description
error (str, optional): Error description
}
```

# Command line usage examples

1.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "Red Square"}' https://varvara-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"location":"Red Square","response":"Temperature: 13C, feels like: 12C, rain."}
```

2.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "Natural History Museum, London"}' https://varvara-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"location":"Natural History Museum, London","response":"Temperature: 20C, feels like: 21C, cloudy."}
```

3.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "Piazza del Colosseo, 1, Roma"}' https://varvara-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"location":"Piazza del Colosseo, 1, Roma","response":"Temperature: 26C, feels like: 28C, clear."}
```

4.

```bash
$ curl -i -H "Content-Type: application/json" -X GET -d '{"location": "хупся"}' https://varvara-weather-forecast-bot.herokuapp.com/weather/api/v1.0/
>> {"error": "Error parsing location 'хупся' with geopy.", "location": "хупся", "response": null}
```

# Used technology stack

1. [Yandex Weather API](https://yandex.ru/dev/weather/): API with detailed weather info based on latitude and longitude
2. [geopy](https://geopy.readthedocs.io/en/stable/): Python library to convert string address to its latitude and longitude
3. [Flask API](https://flask.palletsprojects.com/en/1.1.x/): Web application framework
4. [Docker](https://www.docker.com/): Tool for building containerized applications
5. [Heroku server](https://www.heroku.com/): Cloud server platform
6. [Moesif](https://www.moesif.com/): API Monitoring

# Useful tutorials

1. [Guide to RESTful API with Flask](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
2. [Guide to Deploying a Flask app on Heroku](https://kaushalvivek.github.io/2020-3-30-heroku-flask/)
3. [Yandex Weather API Examples](https://sprut.ai/client/blog/1165)
4. [Heroku Port Binding](https://medium.com/@ksashok/containerise-your-python-flask-using-docker-and-deploy-it-onto-heroku-a0b48d025e43)

# TODO

1. Pre commit hooks 
2. Prometheus
3. Grafana
