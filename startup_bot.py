#!/usr/bin/env python
# import sys
import os
from pathlib import Path
# import logging
import logging.config

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

if __name__ == '__main__':
    pass
