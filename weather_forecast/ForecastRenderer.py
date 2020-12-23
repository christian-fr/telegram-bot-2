import codecs
import os
import datetime
import cairosvg



def datetime_from_unix_timestamp(unix_timestamp):
    assert isinstance(unix_timestamp, int) or isinstance(unix_timestamp, str)
    return datetime.datetime.utcfromtimestamp(unix_timestamp)


def icon_matching_openweather_map(input_icon_code, detailed_weather_code=None):
    matching_dict_ext = {'01d': 'skc.svg', '02d': 'few.svg', '03d': 'sct.svg', '04d': 'bkn.svg', '09d': 'shra.svg',
                     '10d': 'ra.svg', '11d': 'tsra.svg', '13d': 'sn.svg', '50d': 'mist.svg', '01n': 'skc.svg',
                     '02n': 'few.svg', '03n': 'sct.svg', '04n': 'bkn.svg', '09n': 'shra.svg', '10n': 'ra.svg',
                     '11n': 'tsra.svg', '13n': 'sn.svg', '50n': 'mist.svg'}
    matching_dict = {'01d': 'skc', '02d': 'few', '03d': 'sct', '04d': 'bkn', '09d': 'shra',
                     '10d': 'ra', '11d': 'tsra', '13d': 'sn', '50d': 'mist', '01n': 'skc',
                     '02n': 'few', '03n': 'sct', '04n': 'bkn', '09n': 'shra', '10n': 'ra',
                     '11n': 'tsra', '13n': 'sn', '50n': 'mist'}
    if input_icon_code in matching_dict.keys():
        return matching_dict[input_icon_code]
    else:
        raise KeyError(f'Icon code "{input_icon_code}" not found in matching_dict: "{matching_dict.keys()}".')


class WeatherForecastObject:
    def __init__(self, openweather_daily_response):
        self.daily_forecasts_dict = self.create_dict_for_daily_forecast(
            openweather_daily_response.resp_onecall_forecast_dict)

    def create_dict_for_daily_forecast(self, response):
        if 'daily' not in response:
            raise KeyError('Response dict has no key "daily"!')
        else:
            tmp_dict = {}
            for entry in [DailyForecastObject(response_daily_object) for response_daily_object in
                          response['daily']]:
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
        self.weather_icon_svg = icon_matching_openweather_map(self.weather_icon)

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


class ForecastRenderer:
    def __init__(self, svg_template_file, weather_forecast_object, svg_icon_path,
                 forecast_output_filename='forecast_output.svg', forecast_output_path=None):
        assert os.path.exists(svg_icon_path)
        assert os.path.exists(svg_template_file)
        self.svg_template_file = svg_template_file
        assert isinstance(weather_forecast_object, WeatherForecastObject)
        if forecast_output_path is None:
            forecast_output_path = 'output'
        self.svg_template = self.init_svg()
        self.weather_forecast_object = weather_forecast_object
        self.dates = list(weather_forecast_object.daily_forecasts_dict.keys())
        self.dates.sort()
        self.day_one = str(self.dates[0])
        self.svg_modified = self.process_svg(self.svg_template)
        self.write_svg(self.svg_modified, os.path.join(forecast_output_path, forecast_output_filename))
        self.convert_svg_into_png(os.path.join(forecast_output_path, forecast_output_filename))

    def init_svg(self):
        #
        # Preprocess SVG
        #
        # Open SVG to process
        with codecs.open(self.svg_template_file, 'r', encoding='utf-8') as f:
            svg_template = f.read()
        return svg_template

    def process_svg(self, svg_template):
        weekday_dict = {0: 'Mo', 1: 'Di', 2: 'Mi', 3: 'Do', 4: 'Fr', 5: 'Sa', 6: 'So'}

        # # Insert icons and temperatures
        svg_template = svg_template.replace('ICON_ONE', self.weather_forecast_object.daily_forecasts_dict[self.dates[0]].weather_icon_svg)
        svg_template = svg_template.replace('ICON_TWO', self.weather_forecast_object.daily_forecasts_dict[self.dates[1]].weather_icon_svg)
        svg_template = svg_template.replace('ICON_THREE', self.weather_forecast_object.daily_forecasts_dict[self.dates[2]].weather_icon_svg)
        svg_template = svg_template.replace('ICON_FOUR', self.weather_forecast_object.daily_forecasts_dict[self.dates[3]].weather_icon_svg)

        svg_template = svg_template.replace('DAY_TWO', weekday_dict[self.weather_forecast_object.daily_forecasts_dict[self.dates[1]].date.weekday()] + ' ' + self.weather_forecast_object.daily_forecasts_dict[self.dates[1]].date.strftime('%d.%m.'))
        svg_template = svg_template.replace('DAY_THREE', weekday_dict[self.weather_forecast_object.daily_forecasts_dict[self.dates[2]].date.weekday()] + ' ' + self.weather_forecast_object.daily_forecasts_dict[self.dates[2]].date.strftime('%d.%m.'))
        svg_template = svg_template.replace('DAY_FOUR', weekday_dict[self.weather_forecast_object.daily_forecasts_dict[self.dates[3]].date.weekday()] + ' ' + self.weather_forecast_object.daily_forecasts_dict[self.dates[3]].date.strftime('%d.%m.'))

        svg_template = svg_template.replace('HIGH_ONE', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[0]].temp_max))))
        svg_template = svg_template.replace('LOW_ONE', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[0]].temp_min))))

        svg_template = svg_template.replace('HIGH_TWO', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[1]].temp_max))))
        svg_template = svg_template.replace('LOW_TWO', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[1]].temp_min))))

        svg_template = svg_template.replace('HIGH_THREE', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[2]].temp_max))))
        svg_template = svg_template.replace('LOW_THREE', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[2]].temp_min))))

        svg_template = svg_template.replace('HIGH_FOUR', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[3]].temp_max))))
        svg_template = svg_template.replace('LOW_FOUR', str(round(int(self.weather_forecast_object.daily_forecasts_dict[self.dates[3]].temp_min))))

        return svg_template

    @staticmethod
    def write_svg(output_data, output_file):
        # Write output
        print(os.getcwd())
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_data)

    @staticmethod
    def convert_svg_into_png(input_filename, output_filename=None):
        if output_filename is None:
            output_filename = os.path.splitext(input_filename)[0] + '.png'
        cairosvg.svg2png(url=input_filename, write_to=output_filename)


# 'weather-script-preprocess.svg'
