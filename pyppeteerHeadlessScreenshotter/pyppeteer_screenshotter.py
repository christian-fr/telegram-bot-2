from pathlib import Path
import asyncio
from pyppeteer import launch
import os
import logging
from pathlib import Path

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.info('Starting up.')


async def pyppeteer_main(url_str, resolution_dict, output_file):
    assert isinstance(url_str, str)
    assert isinstance(resolution_dict, dict)
    assert isinstance(output_file, str) or isinstance(output_file, Path)
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport(resolution_dict)
    # await page.setViewport({'width': 1920, 'height': 1080})

    template_file = url_str
    print(template_file)
    logger.info('template_file: ' + str(template_file))
    await page.goto('file://'+template_file)

    await page.screenshot({'path': str(output_file)})
    await browser.close()

# asyncio.get_event_loop().run_until_complete(pyppeteer_main(url_str=os.path.abspath(os.path.join(os.path.dirname(__file__), './template.html')), resolution_dict={'width': 1600, 'height': 900}, output_file='example.png'))


