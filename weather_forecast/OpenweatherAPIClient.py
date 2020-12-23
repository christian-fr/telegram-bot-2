# https://blog.seamlesscloud.io/2020/09/be-prepared-for-bad-weather-using-20-lines-of-python/

# icons rendering - kindleb
# https://mpetroff.net/2012/09/kindle-weather-display/

import requests


class OpenWeatherAPICLient:
    def __init__(self, weather_api_key, latitude_str, longitude_str, city_id_str):
        self.resp_current = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?id={city_id_str}&appid={weather_api_key}&units=metric')
        self.resp_onecall_forecast = requests.get(
            f'http://api.openweathermap.org/data/2.5/onecall?lon={longitude_str}&lat={latitude_str}&appid={weather_api_key}&units=metric')
        self.resp_current_dict = json.loads(self.resp_current.text)
        self.resp_onecall_forecast_dict = json.loads(self.resp_onecall_forecast.text)

