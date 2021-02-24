# source: https://gist.github.com/kubinka0505/e2d52058e05646b21c04f6fbe1222b38

__author__ = "kubinka0505, modifications by christian-fr"
__date__ = "07.01.2021"
__version__ = "0.5"
__credits__ = __author__
__status__ = "Development"
__license__ = "Apache 2.0"
__changelog__ = {
    "0.1": ["Initial release"],
    "0.2": [
        "Increased code readability",
        "Easier alignment manipulation",
        "Modified Lines → Images system",
    ],
    "0.3": ["Typo fixes"],
    "0.4": ["Typo fixes"],
    "0.5": ["Fixed an issue where the text line spacing was incorrect if it contained characters of different heights"],
}



"""Simple script providing multiline text draw with emoji support (Pillow & emojicdn)"""
import io
from requests import get
from textwrap import wrap
from urllib.parse import quote_plus
from emoji import emojize, demojize, UNICODE_EMOJI
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError, ImageEnhance, ImageFilter
import numpy as np

# -----#


# -----#

class EmojiUtils:
    """Various emoji utility."""

    # ---#
    def __init__(self, Name: str):
        """Emoji have to start and end with the semicolons!"""
        self.Name = Name

    # ---#
    def get_image(self, Style: int = 5) -> Image.open:
        """Gets Emoji image from "emojicdn.elk.sh" API using style lists from its GitHub main page."""
        Styles = {
            0: 'apple', 1: 'google', 2: 'microsoft', 3: 'samsung',
            4: 'whatsapp', 5: 'twitter', 6: 'facebook',
            7: 'joypixels', 8: 'openmoji', 9: 'emojidex',
            10: 'lg', 11: 'htc', 12: 'mozilla'
        }
        # ---#
        Emoji_Image = Image.open(get(
            "https://emojicdn.elk.sh/{0}?style={1}".format(
                quote_plus(emojize(self.Name, use_aliases=True)),
                str(Styles[Style]).lower()
            ), stream=True
        ).raw
                                 )
        # ---#
        ImageIO = io.BytesIO()
        Emoji_Image.save(ImageIO, "PNG")
        ImageIO.seek(0)
        return Image.open(io.BytesIO(ImageIO.read()))
        ImageIO.close()

    # ---#
    def is_available(Name: str):
        """Checks if emoji is available to use."""
        return emojize(Name, use_aliases=True) in UNICODE_EMOJI

    # ---#
    def search(Name: str):
        """Searches for emojis by `self.Name`."""
        return [x for x in UNICODE_EMOJI.values() if x.__contains__(Name[1:-1])]


# Supported emojis (+ aliases (?)) lists
# https://www.webfx.com/tools/emoji-cheat-sheet/
#
# Supported emoji styles
# https://github.com/benborgers/emojicdn#emoji-style
#
# Check if emoji is available:
# ```python
# >>> Emoji = ":thinking:"
# >>> Emoji = EmojiUtils.search(Emoji)[0]
# >>>
# >>> EmojiUtils.is_available(Emoji)
# True
# ```

# ----------#

def emoji_wrapper(text, text_wrap=70,
                  font_size=250,
                  text_color=(0, 0, 0),
                  shadow_color=(255, 255, 255),
                  font_path=r'/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf',
                  emoji_style="google",
                  image_size=(5000, 5000)):
    # ----------#

    # ----------#

    Base = Image.new("RGBA", image_size, (0,) * 4)

    wrapped_text = wrap(emojize(text, use_aliases=True), text_wrap)
    Font = ImageFont.truetype(font_path, font_size)

    __Styles = {Value: Key for Key, Value in enumerate(EmojiUtils.get_image.__code__.co_consts[1:14])}

    Images_List = []
    Expanded_Images_List = []

    Spacing_Y = 0

    for Line in wrapped_text:
        Line_Image = Base.copy()
        Line_ImageDraw = ImageDraw.Draw(Line_Image)
        Spacing_X = 0
        # ---#
        for Character in Line:
            if Character in UNICODE_EMOJI['en']:
                try:
                    Emoji = EmojiUtils(demojize(Character)).get_image(__Styles[emoji_style])
                except UnidentifiedImageError as Error:
                    raise SystemExit(
                        "{0}: The `{1}` emoji is not supported on the {2} style. Image processing aborted.".format(
                            Error.__class__.__name__,
                            demojize(Character),
                            emoji_style.title(),
                        )
                    )
                # ---#
                Emoji = Emoji.resize(
                    (Font.getsize("|")[1],) * 2,
                    Image.LANCZOS
                )
                # ---#
                Line_Image.paste(
                    Emoji,
                    (Spacing_X, 0),
                    Emoji
                )
                Spacing_X += Emoji.size[0]
                Character = Character.replace(Character, "")
            # ---#
            Line_ImageDraw.text(
                xy=(Spacing_X, 0),
                text=Character,
                font=Font,
                fill=text_color
            )
            # ---#
            Spacing_X += Font.getsize(Character)[0]
        # ---#
        Spacing_Y += Font.getsize(Line)[1]
        Line_Image = Line_Image.crop(Line_Image.getbbox())
        Images_List.append(Line_Image)

    # ---#
    first_run = True
    for IMG in Images_List:

        if first_run:
            Text_Image = Image.new("RGBA", (IMG.size[0], IMG.size[1] + Font.getsize("|")[1]), (0,) * 4)
            Text_Image.paste(IMG, (0, Font.getsize("|")[1]), IMG)
            first_run = False
        else:
            Text_Image = Image.new("RGBA", (IMG.size[0] + font_size, IMG.size[1] + Font.getsize("|")[1]), (0,) * 4)
            Text_Image.paste(IMG, (font_size, Font.getsize("|")[1]), IMG)
        Expanded_Images_List.append(Text_Image)

    Spacing_Y = 0
    for IMG in Expanded_Images_List:
        # Base.paste(IMG, ((Base.size[0] - IMG.size[0]) // 2, Spacing_Y), IMG)
        Base.paste(IMG, (0, Spacing_Y), IMG)
        Spacing_Y += IMG.size[1] // 3 * 2  # Change values for line height

    # ---#

    Base = Base.crop(Base.getbbox())

    data = np.array(Base.copy())  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    # Replace all colors with white (leaves alpha values alone...)
    data[..., :-1] = shadow_color  # Transpose back needed

    white_outline = Image.fromarray(data)

    return Base, white_outline


