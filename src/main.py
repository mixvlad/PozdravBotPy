#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import time
import json
import random

# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

starttime = time.time()
with open('src/data.json') as json_file:
    data = json.load(json_file)

keyboard = []
for greetingCategory in data:
    keyboard.append([InlineKeyboardButton(
        greetingCategory['Type'], callback_data=greetingCategory['Type'])])

reply_markup = InlineKeyboardMarkup(keyboard)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    print(time.time() - starttime)


def get_by_type(greetType):
    """Return a product from the list with given id, or None if not found"""
    return next((p for p in data if p['Type'] == greetType), None)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # query.answer()
    greetingsList = get_by_type(query.data)['Greetings']
    greet = random.choice(greetingsList)
    query.message.reply_text(greet['Text'], reply_markup=reply_markup)

    # query.edit_message_text(text="Selected option: {}".format(query.data))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    TOKEN = os.environ.get('TOKEN', '')
    KWARGS = {"proxy_url": os.environ.get('PROXY_URL', "")}
    PORT = int(os.environ.get('PORT', 8443))
    ENDPOINT = os.environ.get('ENDPOINT')
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, request_kwargs=KWARGS, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen='0.0.0.0',
                          port=PORT,
                          url_path=TOKEN)

    updater.bot.set_webhook(
        ENDPOINT + TOKEN)

    print(time.time() - starttime)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the dftime, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
