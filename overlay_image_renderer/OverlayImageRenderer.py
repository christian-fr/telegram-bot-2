__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "OverlayImageRenderer"


import numpy as np
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import os

import logging

from subprocess import call

from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def datetime_string():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    return dt_string


def overlay_text(background_image_filename, overlay_text_string, overlay_image_filename=None):
    assert isinstance(overlay_text_string, str)
    assert os.path.exists(background_image_filename)
    # font_fname = r'C:\Windows\Fonts\SEGUIEMJ.ttf'
    # font_fname = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    # font_fname = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
    font_fname = os.path.join(os.getcwd(), 'seguiemj.ttf')
    image1 = Image.open(background_image_filename)
    w, h = image1.size
    logger.info("width: {0}px, height: {1}px of uploaded picture".format(str(w), str(h)))
    font_size = round(min(w/20, h/20))
    logger.info("font size: " + str(font_size))
    draw = ImageDraw.Draw(image1)
    print(font_fname)
    font = ImageFont.truetype(font_fname, font_size)
    textcolor = "rgb(0, 0, 0)"
    shadowcolor = "rgb(255, 255, 255)"
    draw_x = round(w/80)
    logger.info("draw_x: " + str(draw_x))
    draw_y = round(h-1.5*font_size)
    logger.info("draw_y: " + str(draw_y))
    logger.info("text position: {0}px, {1}px".format(draw_x, draw_y))
    # draw.text((draw_x-3, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x+3, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y-3), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y+3), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x-2, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x+2, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y-2), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y+2), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x-1, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x+1, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y-1), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y+1), overlay_text_string, font=font, fill=shadowcolor)
    # draw.text((draw_x, draw_y), overlay_text_string, font=font, fill=textcolor)

    pass

    if overlay_image_filename is not None:

        assert os.path.exists(overlay_image_filename)
        overlay_image = Image.open(overlay_image_filename)
        end_size = (1080, 1920)
        background_image = image1.resize(end_size, Image.ANTIALIAS)

        width_background = background_image.size()
        height_background = 0
        width_overlay = 0
        height_overlay = 0
        overlay_position = 0
        background_image.paste(overlay_image, (0,0))
        overlay_image = background_image.copy()
        overlay_image.save(os.path.join(os.path.split(background_image_filename)[0], 'overlay.jpg'))
    image1.save(os.path.join(os.path.split(background_image_filename)[0], 'background.jpg'))
    image1.save(os.path.join(os.path.split(background_image_filename)[0], datetime_string() + '_' + os.path.split(background_image_filename)[1]))


def update_wallpaper():
    call(['bash', '-c', "'/home/pi/lubuntu-wp-changer'"])


# update_wallpaper()


if __name__ == '__main__':
    overlay_text(background_image_filename=os.path.join(os.getcwd(), 'pictures', 'JF4_011336.jpg'),
                 overlay_text_string='xxx',
                 overlay_image_filename=os.path.join(os.getcwd(), 'weather_forecast', 'output', 'forecast_output.png'))

else:
    overlay_text(background_image_filename='/home/christian/PycharmProjects/telegram-bot/pictures/JF4_011336.jpg',
                 overlay_text_string='xxx',
                 overlay_image_filename='/home/christian/PycharmProjects/telegram-bot/weather_forecast/output/forecast_output.png')
