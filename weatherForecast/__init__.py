#!/usr/bin/env python
import os
from pathlib import Path

import weatherForecast.OpenweatherAPIClient
import weatherForecast.ForecastRenderer
import logging

logger = logging.getLogger(__name__)
logger.info('Loading weatherForecast')

svg_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './svg_template'))

if __name__ != '__main__':
    svg_template_file = Path(svg_template_path, 'weather-script-preprocess_inverted.svg')
    logger.info('trying to load svg template file')
    if not svg_template_file.exists():
        logger.error(f'SVG template file not found: "{svg_template_file}"')
        raise FileNotFoundError(f'SVG template file not found: "{svg_template_file}"')

    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    LATITUDE = os.getenv('LATITUDE')
    LONGITUDE = os.getenv('LONGITUDE')
    CITY_ID = os.getenv('CITY_ID')

    # check if all environment variables were set
    if [x for x in (WEATHER_API_KEY, LATITUDE, LONGITUDE, CITY_ID) if x is None]:
        logger.error('Error! One or more environment variable not set:')
        logger.error(
            f'WEATHER_API_KEY: "{WEATHER_API_KEY}", LATITUDE: "{LATITUDE}", '
            f'LONGITUDE: "{LONGITUDE}", 'f'CITY_ID: "{CITY_ID}"')
        raise EnvironmentError('One or more environment variable not found')

    logger.info('firing up weatherForecast.OpenweatherAPIClient.OpenWeatherAPICLient')
    logger.info(f'using weather_api_key: {WEATHER_API_KEY}')
    logger.info(f'using latitude: {LATITUDE}')
    logger.info(f'using longitude: {LONGITUDE}')
    logger.info(f'using city_id: {CITY_ID}')

    openweather_forecast_object = weatherForecast.OpenweatherAPIClient.OpenWeatherAPICLient(
        weather_api_key=WEATHER_API_KEY,
        latitude_str=LATITUDE,
        longitude_str=LONGITUDE,
        city_id_str=CITY_ID)

    logger.info('firing up weatherForecast.OpenweatherAPIClient.OpenWeatherAPICLient')
    weather_forecast_object = weatherForecast.ForecastRenderer.WeatherForecastObject(
        openweather_daily_response=openweather_forecast_object, longitude_str=LONGITUDE, latitude_str=LATITUDE)

    logger.info('firing up weatherForecast.OpenweatherAPIClient.OpenWeatherAPICLient')
    weather_forecast_renderer = weatherForecast.ForecastRenderer.ForecastRenderer(
        svg_template_file=svg_template_file,
        weather_forecast_object=weather_forecast_object)
