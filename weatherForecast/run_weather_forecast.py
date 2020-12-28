__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "WeatherForeCastCreator"

import json
import os

import weatherForecast.ForecastRenderer
import weatherForecast.OpenweatherAPIClient

svg_template_file = os.path.join(os.getcwd(), 'svg_template/weather-script-preprocess_inverted.svg')

key_file = os.path.join(os.getcwd(), 'openweather_api_key.txt')
with open(key_file, 'r') as f:
    tmp_json_string = f.read()

tmp_key_dict = json.loads(tmp_json_string)

WEATHER_API_KEY = tmp_key_dict['WEATHER_API_KEY']
LATITUDE = tmp_key_dict['LATITUDE']
LONGITUDE = tmp_key_dict['LONGITUDE']
CITY_ID = tmp_key_dict['CITY_ID']

# WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
# LATITUDE = os.getenv('LATITUDE')
# LONGITUDE = os.getenv('LONGITUDE')
# BOT_API_KEY = os.getenv('BOT_API_KEY')
# CHANNEL_NAME = os.getenv('CHANNEL_NAME')
# CITY_ID = os.getenv('CITY_ID')


openweather_forecast_object = weatherForecast.OpenweatherAPIClient.OpenWeatherAPICLient(
    weather_api_key=WEATHER_API_KEY,
    latitude_str=LATITUDE,
    longitude_str=LONGITUDE,
    city_id_str=CITY_ID)

weather_forecast_object = weatherForecast.ForecastRenderer.WeatherForecastObject(
    openweather_daily_response=openweather_forecast_object, longitude_str=LONGITUDE, latitude_str=LATITUDE)

weather_forecast_renderer = weatherForecast.ForecastRenderer.ForecastRenderer(
    svg_template_file=svg_template_file,
    weather_forecast_object=weather_forecast_object)
