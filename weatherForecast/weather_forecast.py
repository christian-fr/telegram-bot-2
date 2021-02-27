#!/usr/bin/env python
import os
from pathlib import Path

import weatherForecast.OpenweatherAPIClient
import weatherForecast.ForecastRenderer
import logging


def get_weather_forecast():
    logger = logging.getLogger(__name__)
    logger.info('Loading weatherForecast')

    svg_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './svg_template'))

    svg_template_file = Path(svg_template_path, 'weather-script-preprocess_inverted.svg')
    logger.info('trying to load svg template file')
    if not svg_template_file.exists():
        logger.error(f'SVG template file not found: "{svg_template_file}"')
        raise FileNotFoundError(f'SVG template file not found: "{svg_template_file}"')

    logger.info('firing up weatherForecast.OpenweatherAPIClient.OpenWeatherAPICLient')

    openweather_forecast_object = weatherForecast.OpenweatherAPIClient.OpenWeatherAPIClient()

    logger.info('firing up weatherForecast.OpenweatherAPIClient.OpenWeatherAPIClient')
    weather_forecast_object = weatherForecast.ForecastRenderer.WeatherForecastObject(
        openweather_daily_response=openweather_forecast_object)

    logger.info('firing up weatherForecast.OpenweatherAPIClient.OpenWeatherAPIClient')
    weatherForecast.ForecastRenderer.ForecastRenderer(
        svg_template_file=svg_template_file,
        weather_forecast_object=weather_forecast_object,
        forecast_output_path=os.path.join(os.getcwd(), 'output_forecast'))
