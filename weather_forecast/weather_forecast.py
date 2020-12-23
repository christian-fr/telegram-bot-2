# https://blog.seamlesscloud.io/2020/09/be-prepared-for-bad-weather-using-20-lines-of-python/

# icons rendering - kindleb
# https://mpetroff.net/2012/09/kindle-weather-display/

import os
import json
import datetime
import requests


def datetime_from_unix_timestamp(unix_timestamp):
    assert isinstance(unix_timestamp, int) or isinstance(unix_timestamp, str)
    return datetime.datetime.utcfromtimestamp(unix_timestamp)


def create_dict_for_daily_forecast(response_dict):
    if 'daily' not in response_dict:
        raise KeyError('Response dict has no key "daily"!')
    else:
        tmp_dict = {}
        for entry in [DailyForecastObject(response_daily_object) for response_daily_object in resp_onecall_forecast_dict['daily']]:
            assert isinstance(entry, DailyForecastObject)
            tmp_dict[entry.date] = entry

    return tmp_dict


class DailyForecastObject:
    def __init__(self, response_daily_object):
        self.timestamp_raw = response_daily_object['dt']
        self.timestamp = datetime_from_unix_timestamp(response_daily_object['dt'])
        self.date = self.timestamp.date()
        self.sunset_raw = response_daily_object['sunset']
        self.sunset = datetime_from_unix_timestamp(response_daily_object['sunset'])
        self.sunrise_raw = response_daily_object['sunrise']
        self.sunrise = datetime_from_unix_timestamp(response_daily_object['sunrise'])

        self.weather_desc = response_daily_object['weather'][0]['description']
        self.weather_icon = response_daily_object['weather'][0]['icon']
        self.weather_main = response_daily_object['weather'][0]['main']
        self.weather_id = response_daily_object['weather'][0]['id']
        self.temp_feel_day = response_daily_object['feels_like']['day']
        self.temp_feel_night = response_daily_object['feels_like']['night']
        self.temp_feel_evening = response_daily_object['feels_like']['eve']
        self.temp_feel_morning = response_daily_object['feels_like']['morn']
        self.temp_day = response_daily_object['temp']['day']
        self.temp_night = response_daily_object['temp']['night']
        self.temp_evening = response_daily_object['temp']['eve']
        self.temp_morning = response_daily_object['temp']['morn']
        self.temp_min = response_daily_object['temp']['min']
        self.temp_max = response_daily_object['temp']['max']
        self.wind_speed = response_daily_object['wind_speed']

        if 'rain' in response_daily_object:
            self.rain = response_daily_object['rain']
        else:
            self.rain = None

        if 'clouds' in response_daily_object:
            self.clouds = response_daily_object['clouds']
        else:
            self.clouds = None

        self.humidity = response_daily_object['humidity']


key_file = '/home/christian/PycharmProjects/telegram-bot/weather_forecast/openweather_api_key.txt'
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






if __name__ == '__main__':
    resp_current = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={WEATHER_API_KEY}&units=metric')
    resp_onecall_forecast = requests.get(f'http://api.openweathermap.org/data/2.5/onecall?lon={LONGITUDE}&lat={LATITUDE}&appid={WEATHER_API_KEY}&units=metric')
    resp_current_dict = json.loads(resp_current.text)
    resp_onecall_forecast_dict = json.loads(resp_onecall_forecast.text)
    b = create_dict_for_daily_forecast(resp_onecall_forecast_dict)


