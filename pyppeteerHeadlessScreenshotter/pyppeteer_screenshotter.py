from pathlib import Path
import asyncio
from pyppeteer import launch
import os
import logging

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.info('Starting up.')


async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1600, 'height': 900})
    # await page.setViewport({'width': 1920, 'height': 1080})

    template_file = os.path.abspath(os.path.join(os.path.dirname(__file__), './template.html'))
    print(template_file)
    logger.info('template_file: ' + str(template_file))
    await page.goto('file://'+template_file)

    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
