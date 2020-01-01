with open(r'token', 'r') as f:
    token = f.readline()
    # print(token)

import os
from telegram.ext import Updater
from telegram.ext import filters


updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start, filters.Filters.user(username='@pythonista123'))
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    myCmd = 'youtube-dl -x ' + update.message.text
    os.system(myCmd)
    myCmd = 'mv *.opus /media/usb-hdd/Musik/_temp && mpc update _temp'
    os.system(myCmd)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo, Filters.user(username='@pythonista123'))

dispatcher.add_handler(echo_handler)

updater.start_polling()