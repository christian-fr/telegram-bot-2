__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "OpenWeatherAPIClient"

import requests
import json
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class OpenWeatherSettings:
    openweather_secrets_file: Path = Path(os.environ.get(
        "OPENWEATHER_CONFIG_PATH", os.path.expanduser("~/.local/share/openweather/openweather_config.json")
    ))
    assert openweather_secrets_file.exists()
    secrets_dict = json.loads(openweather_secrets_file.read_text())
    weather_api_key = secrets_dict["WEATHER_API_KEY"]
    latitude = secrets_dict["LATITUDE"]
    longitude = secrets_dict["LONGITUDE"]
    city_id = secrets_dict["CITY_ID"]


open_weather_settings = OpenWeatherSettings()


class OpenWeatherAPIClient:
    def __init__(self, openweather_settings: OpenWeatherSettings = OpenWeatherSettings()):

        self.resp_current = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?id={openweather_settings.city_id}&appid={openweather_settings.weather_api_key}&units=metric')
        self.resp_onecall_forecast = requests.get(
            f'http://api.openweathermap.org/data/2.5/onecall?lon={openweather_settings.longitude}&lat={openweather_settings.latitude}&appid={openweather_settings.weather_api_key}&units=metric')
        self.resp_current_dict = json.loads(self.resp_current.text)
        self.resp_onecall_forecast_dict = json.loads(self.resp_onecall_forecast.text)
        self.resp_onecall_forecast_dict['latitude_str'] = openweather_settings.latitude
        self.resp_onecall_forecast_dict['longitude_str'] = openweather_settings.longitude


# OpenWeatherAPIClient(OpenWeatherSettings())
