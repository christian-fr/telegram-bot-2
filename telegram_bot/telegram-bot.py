#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Christian Friedrich"
__maintainer__ = "Christian Friedrich"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Prototype"
__name__ = "TelegramBot"



with open(r'token', 'r') as f:
    token = f.readline().strip()


"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import numpy as np
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import logging

from subprocess import call

from datetime import datetime

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PHOTO, DESCRIPTION = range(2)


def datetime_string():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    return dt_string


def overlay_text(filename, overlay_text_string):
    assert isinstance(overlay_text_string, str) and isinstance(filename, str)
    # font_fname = r'C:\Windows\Fonts\SEGUIEMJ.ttf'
    # font_fname = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    # font_fname = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
    font_fname = '/home/christian/seguiemj.ttf'
    image1 = Image.open(filename)
    w, h = image1.size
    logger.info("width: {0}px, height: {1}px of uploaded picture".format(str(w), str(h)))
    font_size = round(min(w/20, h/20))
    logger.info("font size: " + str(font_size))

    draw = ImageDraw.Draw(image1)

    font = ImageFont.truetype(font_fname, font_size)

    textcolor = "rgb(0, 0, 0)"
    shadowcolor = "rgb(255, 255, 255)"
    draw_x = round(w/80)
    logger.info("draw_x: " + str(draw_x))
    draw_y = round(h-1.5*font_size)
    logger.info("draw_y: " + str(draw_y))
    logger.info("text position: {0}px, {1}px".format(draw_x, draw_y))
    draw.text((draw_x-1, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    draw.text((draw_x+1, draw_y), overlay_text_string, font=font, fill=shadowcolor)
    draw.text((draw_x, draw_y-1), overlay_text_string, font=font, fill=shadowcolor)
    draw.text((draw_x, draw_y+1), overlay_text_string, font=font, fill=shadowcolor)
    draw.text((draw_x, draw_y), overlay_text_string, font=font, fill=textcolor)
    image1.save(datetime_string() + '.jpg')
    image1.save('background.jpg')

def update_wallpaper():
    call(['bash', '-c', "'/home/christian/lubuntu-wp-changer'"])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please upload a picture',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('background.jpg')
    logger.info("Picture uploaded!")
    tmp_text = user.first_name
    overlay_text(filename='../background.jpg', overlay_text_string=tmp_text)
    update_wallpaper()

    update.message.reply_text(
        'You have some notes to add to the picture?'
    )

    return DESCRIPTION


def description(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("notes: %s, user: %s", update.message.text, user.first_name)
    tmp_text = user.first_name + ': ' + update.message.text
    update.message.reply_text('Notes successfully added.')
    overlay_text(filename='../background.jpg', overlay_text_string=tmp_text)
    update_wallpaper()
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    # user = update.message.from_user
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo)],
            DESCRIPTION: [MessageHandler(Filters.text, description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
