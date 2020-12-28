__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "OverlayImageRenderer"

# import numpy as np
# import PIL
import PIL.Image as Image
# import PIL.ImageDraw as ImageDraw
# import PIL.ImageFont as ImageFont
import os

import logging

from subprocess import call

from datetime import datetime

logger = logging.getLogger(__name__)


def datetime_string():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    return dt_string


def overlay_text(background_image_filename, overlay_text_string, overlay_image_filename=None,
                 end_height=1080, end_width=1920, horizontal_centering=True):
    assert isinstance(end_width, int) and isinstance(end_height, int)
    assert isinstance(overlay_text_string, str)
    assert os.path.exists(background_image_filename)
    font_fname = os.getenv('FONT_FILE')

    background_image = Image.open(background_image_filename)
    w, h = background_image.size
    logger.info("width: {0}px, height: {1}px of uploaded picture".format(str(w), str(h)))
    font_size = round(min(w / 20, h / 20))
    logger.info("font size: " + str(font_size))
    # draw = ImageDraw.Draw(background_image)
    # font = ImageFont.truetype(font_fname, font_size)
    # text_color = "rgb(0, 0, 0)"
    # shadow_color = "rgb(255, 255, 255)"
    draw_x = round(w / 80)
    logger.info("draw_x: " + str(draw_x))
    draw_y = round(h - 1.5 * font_size)
    logger.info("draw_y: " + str(draw_y))
    logger.info("text position: {0}px, {1}px".format(draw_x, draw_y))

    # draw.text((draw_x-3, draw_y), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x+3, draw_y), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y-3), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y+3), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x-2, draw_y), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x+2, draw_y), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y-2), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y+2), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x-1, draw_y), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x+1, draw_y), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y-1), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y+1), overlay_text_string, font=font, fill=shadow_color)
    # draw.text((draw_x, draw_y), overlay_text_string, font=font, fill=text_color)

    pass

    # resize background image to fit end_size

    rgb_color_of_empty_background = (0, 0, 0)
    image_border_width = {'l': 20, 't': 20, 'r': 20, 'b': 20, 'right_margin': 800}
    resulting_image_width = end_width - image_border_width['l'] - image_border_width['r'] - image_border_width[
        'right_margin']
    resulting_image_height = end_height - image_border_width['t'] - image_border_width['b']

    resulting_imagesize_ratio_width_per_height = end_width / end_height

    background_image_size_ratio_width_per_height = background_image.size[0] / background_image.size[1]

    background_image_resized = None
    if background_image_size_ratio_width_per_height < resulting_imagesize_ratio_width_per_height:
        background_image_resized = background_image.resize(
            (round(resulting_image_height * background_image_size_ratio_width_per_height), resulting_image_height),
            Image.ANTIALIAS).copy()
    elif background_image_size_ratio_width_per_height > resulting_imagesize_ratio_width_per_height:
        background_image_resized = background_image.resize(
            (resulting_image_width, resulting_image_height / background_image_size_ratio_width_per_height),
            Image.ANTIALIAS).copy()
        raise NotImplementedError('')
    elif background_image_size_ratio_width_per_height == resulting_imagesize_ratio_width_per_height:
        background_image_resized = background_image.resize((resulting_image_width, resulting_image_height),
                                                           Image.ANTIALIAS).copy()
        raise NotImplementedError('')

    empty_background_end_size = Image.new('RGB', (end_width, end_height), rgb_color_of_empty_background)
    empty_background_end_size.save('test.png')

    if horizontal_centering is True:
        width_left_for_image = end_width - image_border_width['l'] - image_border_width['r'] - image_border_width[
            'right_margin']
        spare_width = width_left_for_image - background_image_resized.size[0]
        resulting_image_border_width_left = round(spare_width / 2)

    else:
        resulting_image_border_width_left = image_border_width['l']

    # resize overlay image to fit into right margin (border)

    overlay_image_resized = None
    if overlay_image_filename is not None:
        assert os.path.exists(overlay_image_filename)

        resulting_overlay_image_max_height = end_height - image_border_width['t'] - image_border_width['b']
        resulting_overlay_image_max_width = image_border_width['right_margin']

        overlay_image = Image.open(overlay_image_filename)
        overlay_image_ratio_width_per_height = overlay_image.size[0] / overlay_image.size[1]

        overlay_image_resized = overlay_image.resize((resulting_overlay_image_max_width, round(
            resulting_overlay_image_max_width / overlay_image_ratio_width_per_height)), Image.ANTIALIAS).copy()

        overlay_image_resized.save('test3.png')
        print('done')

        # width_background = background_image.size
        # height_background = 0
        #
        # background_image_resized = background_image.resize((end_width, end_height), Image.ANTIALIAS).copy()

        # width_overlay = 0
        # height_overlay = 0
        # overlay_position = 0
        # background_image_resized.paste(overlay_image, (0, 0))
        # overlay_image = background_image_resized.copy()
        # overlay_image.save(os.path.join(os.path.split(background_image_filename)[0], 'overlay.jpg'))

    empty_background_end_size.paste(background_image_resized,
                                    (resulting_image_border_width_left, image_border_width['t']))

    if overlay_image_filename is not None:
        empty_background_end_size.paste(overlay_image_resized, (
        empty_background_end_size.size[0] - overlay_image_resized.size[0], image_border_width['t']))

    empty_background_end_size.save('test2.png')
    print('done')

    background_image.save(os.path.join(os.path.split(background_image_filename)[0], 'background.jpg'))
    background_image.save(os.path.join(os.path.split(background_image_filename)[0],
                                       datetime_string() + '_' + os.path.split(background_image_filename)[1]))


def update_wallpaper():
    call(['bash', '-c', "'/home/pi/lubuntu-wp-changer'"])


if __name__ == '__main__':
    logger.error('Tried to run python script standalone - not yet implemented.')
    raise NotImplementedError('running standalone is not yet implemented')
    pass
    # overlay_text(background_image_filename=os.path.join(os.getcwd(), 'pictures', 'JF4_011336.jpg'),
    #              overlay_text_string='xxx',
    #              overlay_image_filename=os.path.join(os.getcwd(), 'weatherForecast', 'output', 'forecast_output.png'))
else:
    pass