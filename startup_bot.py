#!/usr/bin/env python
# import sys
import os
from pathlib import Path
import logging.config
from subprocess import call

config_filename = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'logger.config')))
assert config_filename.exists()
logging.config.fileConfig(fname=config_filename, disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.info('Starting up.')

import weatherForecast
# from weatherForecast import ForecastRenderer, OpenweatherAPIClient
from overlayImageRenderer import OverlayImageRenderer

# import telegramBot
# from telegramBot import telegram-bot # usw.usf.


# set output path / get an absolute path
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './output'))
pictures_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pictures'))
background_file = Path(pictures_path, 'background.png')
wallpaper_changer_file = os.path.abspath(os.path.join(os.path.dirname(__file__), './wallpaper_changer.sh'))

def update_wallpaper():
    logger.info(f'changing wallpaper to: "{wallpaper_changer_file}"')
    call(['bash', '-c', f"'{wallpaper_changer_file}'"])


if __name__ == '__main__':
    pass
    OverlayImageRenderer.overlay_text(background_image_filename=Path(pictures_path, 'input.png'),
                                      overlay_text_string='xxx',
                                      overlay_image_filename=Path(output_path, 'forecast_output.png'),
                                      output_file=background_file)

    update_wallpaper()
    exit()
