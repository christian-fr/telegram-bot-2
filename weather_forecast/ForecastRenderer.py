import os
import datetime


def datetime_from_unix_timestamp(unix_timestamp):
    assert isinstance(unix_timestamp, int) or isinstance(unix_timestamp, str)
    return datetime.datetime.utcfromtimestamp(unix_timestamp)


def icon_matching_openweather_map(input_icon_code, path_to_svg_files, detailed_weather_code=None):
    matching_dict = {'01d': 'skc.svg', '02d': 'few.svg', '03d': 'sct.svg', '04d': 'bkn.svg', '09d': 'shra.svg',
                     '10d': 'ra.svg', '11d': 'tsra.svg', '13d': 'sn.svg', '50d': 'mist.svg', '01n': 'skc.svg',
                     '02n': 'few.svg', '03n': 'sct.svg', '04n': 'bkn.svg', '09n': 'shra.svg', '10n': 'ra.svg',
                     '11n': 'tsra.svg', '13n': 'sn.svg', '50n': 'mist.svg'}
    if input_icon_code in matching_dict.keys():
        return os.path.join(path_to_svg_files, matching_dict[input_icon_code])
    else:
        raise KeyError(f'Icon code "{input_icon_code}" not found in matching_dict: "{matching_dict.keys()}".')


def create_dict_for_daily_forecast(response_dict):
    if 'daily' not in response_dict:
        raise KeyError('Response dict has no key "daily"!')
    else:
        tmp_dict = {}
        for entry in [DailyForecastObject(response_daily_object, svg_path) for response_daily_object in
                      resp_onecall_forecast_dict['daily']]:
            assert isinstance(entry, DailyForecastObject)
            tmp_dict[entry.date] = entry

    return tmp_dict


class DailyForecastObject:
    def __init__(self, response_daily_object, path_to_svg_files):
        self.timestamp_raw = response_daily_object['dt']
        self.timestamp = datetime_from_unix_timestamp(response_daily_object['dt'])
        self.date = self.timestamp.date()
        self.sunset_raw = response_daily_object['sunset']
        self.sunset = datetime_from_unix_timestamp(response_daily_object['sunset'])
        self.sunrise_raw = response_daily_object['sunrise']
        self.sunrise = datetime_from_unix_timestamp(response_daily_object['sunrise'])

        self.weather_desc = response_daily_object['weather'][0]['description']
        self.weather_icon = response_daily_object['weather'][0]['icon']
        self.weather_icon_svg = icon_matching_openweather_map(self.weather_icon, path_to_svg_files)

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


