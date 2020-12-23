import json
import os

import weather_forecast.ForecastRenderer
import weather_forecast.OpenweatherAPIClient

svg_path = os.path.join(os.getcwd(), 'icons')
svg_template_file = os.path.join(os.getcwd(), 'svg_template/weather-script-preprocess.svg')

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


openweather_forecast_object = weather_forecast.OpenweatherAPIClient.OpenWeatherAPICLient(
    weather_api_key=WEATHER_API_KEY,
    latitude_str=LATITUDE,
    longitude_str=LONGITUDE,
    city_id_str=CITY_ID)

weather_forecast_object = weather_forecast.ForecastRenderer.WeatherForecastObject(openweather_forecast_object)

weather_forecast_renderer = weather_forecast.ForecastRenderer.ForecastRenderer(
    svg_template_file=svg_template_file,
    weather_forecast_object=weather_forecast_object,
    svg_icon_path=svg_path)
pass
