__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "OverlayImageRenderer"

import PIL.Image as Image
import PIL.ImageFont as ImageFont
import os
import logging
from datetime import datetime
from . import emojiWrapper

logger = logging.getLogger(__name__)


def datetime_string():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    return dt_string


def overlay_text(background_image_filename, overlay_text_string, output_file, font_file, overlay_image_filename=None,
                 end_height=1080, end_width=1920, horizontal_centering=True):
    assert isinstance(end_width, int) and isinstance(end_height, int)
    assert isinstance(overlay_text_string, str)
    logger.info(f'background_image_filename: {background_image_filename}')
    assert os.path.exists(background_image_filename)
    font_fname = font_file

    background_image = Image.open(background_image_filename)
    w, h = background_image.size
    logger.info("width: {0}px, height: {1}px of uploaded picture".format(str(w), str(h)))
    font_size = round(min(w / 20, h / 20))
    logger.info("font size: " + str(font_size))

    font = ImageFont.truetype(font_fname, font_size)
    text_color = (0, 0, 0)
    shadow_color = (255, 255, 255)
    draw_x = round(w / 80)
    logger.info("draw_x: " + str(draw_x))
    draw_y = round(h - 1.5 * font_size)
    logger.info("draw_y: " + str(draw_y))

    rendered_text, shadow_outline = emojiWrapper.emoji_wrapper(text=overlay_text_string,
                                                               text_color=text_color,
                                                               shadow_color=shadow_color)
    rendered_text.thumbnail((background_image.size[0]*.8, background_image.size[1]*.2))
    shadow_outline.thumbnail((background_image.size[0]*.8, background_image.size[1]*.2))

    paste_x = round(background_image.size[0]*0.05)
    paste_y = round(background_image.size[1]-rendered_text.size[1]-background_image.size[1]*0.05)
    logger.info("text position: {0}px, {1}px".format(draw_x, draw_y))

    for jitter in [0.002, 0.001]:
        background_image.paste(shadow_outline, (round(paste_x+(max(background_image.size)*jitter)), round(paste_y+(max(background_image.size)*jitter))), shadow_outline)
        background_image.paste(shadow_outline, (round(paste_x-(max(background_image.size)*jitter)), round(paste_y-(max(background_image.size)*jitter))), shadow_outline)
        background_image.paste(shadow_outline, (round(paste_x+(max(background_image.size)*jitter)), round(paste_y-(max(background_image.size)*jitter))), shadow_outline)
        background_image.paste(shadow_outline, (round(paste_x-(max(background_image.size)*jitter)), round(paste_y+(max(background_image.size)*jitter))), shadow_outline)

    for jitter in [0.0025]:
        background_image.paste(shadow_outline, (paste_x, round(paste_y + (max(background_image.size) * jitter))), shadow_outline)
        background_image.paste(shadow_outline, (paste_x, round(paste_y - (max(background_image.size) * jitter))), shadow_outline)
        background_image.paste(shadow_outline, (round(paste_x + (max(background_image.size) * jitter)), paste_y), shadow_outline)
        background_image.paste(shadow_outline, (round(paste_x - (max(background_image.size) * jitter)), paste_y), shadow_outline)

    background_image.paste(rendered_text, (paste_x, paste_y), rendered_text)
    # background_image.show()

    background_image.save(output_file)


if __name__ == '__main__':
    logger.error('Tried to run python script standalone - not yet implemented.')
    raise NotImplementedError('running standalone is not yet implemented')

