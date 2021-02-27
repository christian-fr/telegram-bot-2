#!/usr/bin/env python
# import sys
import sys
import os
from pathlib import Path
import logging.config
# from subprocess import call
import pyppeteerHeadlessScreenshotter.pyppeteer_screenshotter
import asyncio
# import json
from weatherForecast import weather_forecast
# from overlayImageRenderer import OverlayImageRenderer
# from pydantic import BaseSettings

weather_forecast.get_weather_forecast()

config_filename = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'logger.config')))
assert config_filename.exists()
logging.config.fileConfig(fname=config_filename, disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.info('Starting up.')

# set output path / get an absolute path
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output_forecast'))
pictures_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output_background_image'))
background_file = Path(pictures_path, 'background.png')
wallpaper_changer_file = os.path.abspath(os.path.join(os.path.dirname(__file__), './wallpaper_changer.sh'))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        pyppeteerHeadlessScreenshotter.pyppeteer_screenshotter.pyppeteer_main(
            executable_path='/usr/bin/chromium-browser', url_str=os.path.abspath(
                os.path.join(os.path.dirname(__file__), './pyppeteerHeadlessScreenshotter/template.html')),
            resolution_dict={'width': 1600,
                             'height': 900},
            output_file='output_background_image/background_final.png'))
    sys.exit()
