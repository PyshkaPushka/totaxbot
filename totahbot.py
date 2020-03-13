#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, datetime, re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatPermissions, MessageEntity

DEFAULT_TOTAH_LEVEL = 60

gulag = {}

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
    update.message.reply_text('Можешь попробовать:\n\t/totah <сколько балов>\n\t/totahsheli <@ми тотах шель аба>\n')


def beria_who_is_this_spy(username):
    if username in gulag:
        return gulag[username]
    return None


def beria(update, context):
    username = update.message.from_user.username
    if username is not None and username not in gulag:
        gulag[username] = update.message.from_user


def totah(update, context):
    update.message.reply_text("Курцер тотах!")


def totah_command(update, context):
    totah_level = 0
    if len(context.args) >= 1:
        totah_level = int(context.args[0])

    apply_totah_level(totah_level, update.message.from_user, update, context)


def get_totah_shel_aba(message):
    for e in message.entities:
        if e.type == MessageEntity.TEXT_MENTION:
            return e.user
        if e.type == MessageEntity.MENTION:
            username = message.parse_entity(e)[1:]  # remove @ in front of username
            return beria_who_is_this_spy(username)

    return None


def totah_sheli_command(update, context):
    mi_totah_shel_aba = get_totah_shel_aba(update.message)

    if mi_totah_shel_aba is None:
        update.message.reply_text("Я не понял, а кто тотах то?")
        return

    apply_totah_level(DEFAULT_TOTAH_LEVEL, mi_totah_shel_aba, update, context)


def get_totah_permissions():
    return ChatPermissions(can_send_messages=False,
                           can_change_info=False,
                           can_invite_users=False,
                           can_send_media_messages=False,
                           can_send_polls=False,
                           can_send_other_messages=False,
                           can_add_web_page_previews=False,
                           can_pin_messages=False)


def apply_totah_level(totah_level, user, update, context):
    if totah_level < 1:
        totah_level = DEFAULT_TOTAH_LEVEL

    until = datetime.datetime.utcnow() + datetime.timedelta(minutes=totah_level)

    permissions = get_totah_permissions()

    name = user.first_name
    if user.username is not None:
        name += ' "' + user.username + '"'
    if user.last_name is not None:
        name += " " + user.last_name

    update.message.reply_text('{0} будет тотахом аж на {1}!'.format(name, totah_level))

    context.bot.restrict_chat_member(update.message.chat_id, user.id, permissions, until_date=until)


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
    dp.add_handler(CommandHandler("totahsheli", totah_sheli_command))

    # handle text messages
    dp.add_handler(MessageHandler(Filters.regex(re.compile(r'курцер', re.IGNORECASE)), totah))
    dp.add_handler(MessageHandler(Filters.text, beria))

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
