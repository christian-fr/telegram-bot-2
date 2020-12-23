import os
import json
import openweather_api_client
import ForecastRenderer


svg_path = os.path.join(os.getcwd(), 'weather_forecast', 'icons')


key_file = os.path.join(os.getcwd(), 'weather_forecast', 'openweather_api_key.txt')
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


OpenWeatherAPICLient(weather_api_key, latitude_str, longitude_str, city_id_str)