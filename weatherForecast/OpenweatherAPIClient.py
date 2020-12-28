__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "OpenWeatherAPIClient"

import requests
import json
import logging

logger = logging.getLogger(__name__)

class OpenWeatherAPICLient:
    def __init__(self, weather_api_key, latitude_str, longitude_str, city_id_str):
        self.resp_current = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?id={city_id_str}&appid={weather_api_key}&units=metric')
        self.resp_onecall_forecast = requests.get(
            f'http://api.openweathermap.org/data/2.5/onecall?lon={longitude_str}&lat={latitude_str}&appid={weather_api_key}&units=metric')
        self.resp_current_dict = json.loads(self.resp_current.text)
        self.resp_onecall_forecast_dict = json.loads(self.resp_onecall_forecast.text)
        self.resp_onecall_forecast_dict['latitude_str'] = latitude_str
        self.resp_onecall_forecast_dict['longitude_str'] = longitude_str
