#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatPermissions

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Категорически приветсвую!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Можешь попробовать:\n\t/totah <сколько балов>')


def totah(update, context):
    if any(text in update.message.text for text in ["Курцер", "курцер"]):
      update.message.reply_text("Курцер тотах!")


def totah_command(update, context):
    totah_level = 0

    if len(context.args) >= 1:
        totah_level = int(context.args[0])

    if totah_level < 1:
        totah_level = 60

    until = datetime.datetime.utcnow() + datetime.timedelta(minutes = totah_level)

    permissions = ChatPermissions(can_send_messages=False,
                                  can_change_info=False,
                                  can_invite_users=False,
                                  can_send_media_messages=False,
                                  can_send_polls=False,
                                  can_send_other_messages=False,
                                  can_add_web_page_previews=False,
                                  can_pin_messages=False)

    user = update.message.from_user.first_name + (update.message.from_user.last_name if update.message.from_user.last_name != None else "")

    update.message.reply_text('{0} будет тотахом аж на {1}!'.format(user, totah_level))

    context.bot.restrict_chat_member(update.message.chat_id, update.message.from_user.id, permissions, until_date=until)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("<secret-token>", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("totah", totah_command))

    # handle text messages
    dp.add_handler(MessageHandler(Filters.text, totah))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
