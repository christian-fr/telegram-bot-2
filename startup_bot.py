#!/usr/bin/env python
# import sys
import sys
import os
from pathlib import Path
import logging.config
from subprocess import call
import pyppeteerHeadlessScreenshotter.pyppeteer_screenshotter
import asyncio
import json
from weatherForecast import run_weather_forecast
from overlayImageRenderer import OverlayImageRenderer
from pydantic import BaseSettings
import json

run_weather_forecast.get_weather_forecast()

config_filename = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'logger.config')))
assert config_filename.exists()
logging.config.fileConfig(fname=config_filename, disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.info('Starting up.')

# import telegramBot
# from telegramBot import telegram-bot # usw.usf.






# ToDo: implement within BaseSettings
#
# set output path / get an absolute path
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './output'))
pictures_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pictures'))
background_file = Path(pictures_path, 'background.png')
wallpaper_changer_file = os.path.abspath(os.path.join(os.path.dirname(__file__), './wallpaper_changer.sh'))

if __name__ == '__main__':
    pass
    # OverlayImageRenderer.overlay_text(background_image_filename=Path(pictures_path, 'background_input.png'),
    #                                   overlay_text_string='xxx',
    #                                   overlay_image_filename=Path(output_path, 'forecast_output.png'),
    #                                   output_file=background_file)

    # update_wallpaper()

    asyncio.get_event_loop().run_until_complete(
        pyppeteerHeadlessScreenshotter.pyppeteer_screenshotter.pyppeteer_main(
            executable_path='/usr/bin/chromium-browser', url_str=os.path.abspath(
                os.path.join(os.path.dirname(__file__), './pyppeteerHeadlessScreenshotter/template.html')),
            resolution_dict={'width': 1600,
                             'height': 900},
            output_file='pictures/background_final.png'))
    sys.exit()
