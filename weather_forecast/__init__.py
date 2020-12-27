#!/usr/bin/env python
import os
from pathlib import Path

import weather_forecast.OpenweatherAPIClient
# import weather_forecast.ForecastRenderer

svg_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './svg_template'))

if __name__ != '__main__':

    svg_template_file = Path(svg_template_path, 'weather-script-preprocess_inverted.svg')
    if not svg_template_file.exists():
        raise FileNotFoundError(f'SVG template file not found: "{svg_template_file}"')

    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    LATITUDE = os.getenv('LATITUDE')
    LONGITUDE = os.getenv('LONGITUDE')
    CITY_ID = os.getenv('CITY_ID')

    # check if all environment variables were set
    if [x for x in (WEATHER_API_KEY, LATITUDE, LONGITUDE, CITY_ID) if x is None]:
        print('Error! One or more environment variable not set:')
        print(f'WEATHER_API_KEY: "{WEATHER_API_KEY}", LATITUDE: "{LATITUDE}", LONGITUDE: "{LONGITUDE}", '
              f'CITY_ID: "{CITY_ID}"')
        raise EnvironmentError('One or more environment variable not found')

    openweather_forecast_object = weather_forecast.OpenweatherAPIClient.OpenWeatherAPICLient(
        weather_api_key=WEATHER_API_KEY,
        latitude_str=LATITUDE,
        longitude_str=LONGITUDE,
        city_id_str=CITY_ID)

    # weather_forecast_object = weather_forecast.ForecastRenderer.WeatherForecastObject(
    #     openweather_daily_response=openweather_forecast_object, longitude_str=LONGITUDE, latitude_str=LATITUDE)

    # weather_forecast_renderer = weather_forecast.ForecastRenderer.ForecastRenderer(
    #     svg_template_file=svg_template_file,
    #     weather_forecast_object=weather_forecast_object)

