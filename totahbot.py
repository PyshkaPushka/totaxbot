#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, datetime, re, sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatPermissions, MessageEntity
from pollhandler import PollHandler

DEFAULT_TOTAH_LEVEL = 60
POLL_TIME = 5

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
    update.message.reply_text("""Можешь попробовать:
\t/totah <сколько балов>
\t/totahsheli <@ми тотах шель аба>
\t/totahsheli Ja""")


def beria_postroy_gulag(context):
    context.chat_data['gulag'] = {'ids': {}, 'usernames': {}}


def beria_how_many_spies(context):
    if 'gulag' in context.chat_data:
        return len(context.chat_data['gulag']['ids'])
    beria_postroy_gulag(context)
    return 0


def beria_who_is_this_spy(username, context):
    if 'gulag' in context.chat_data and username in context.chat_data['gulag']['usernames']:
        return context.chat_data['gulag']['usernames'][username]
    return None


def beria(update, context):
    username = update.message.from_user.username
    id = update.message.from_user.id
    if 'gulag' not in context.chat_data:
        beria_postroy_gulag(context)
    if username is not None and username not in context.chat_data['gulag']['usernames']:
        context.chat_data['gulag']['usernames'][username] = update.message.from_user
    context.chat_data['gulag']['ids'][id] = 1


def totah(update, context):
    update.message.reply_text("Курцер тотах!")


def totah_command(update, context):
    totah_level = 0
    if len(context.args) >= 1:
        totah_level = int(context.args[0])

    apply_totah_level(totah_level, update.message.from_user, update.message, context)


def get_totah_shel_aba(message, context):
    if len(context.args) >= 1:
        if context.args[0].lower() == "ja":
            return message.from_user

    for e in message.entities:
        if e.type == MessageEntity.TEXT_MENTION:
            return e.user
        if e.type == MessageEntity.MENTION:
            username = message.parse_entity(e)[1:]  # remove @ in front of username
            return beria_who_is_this_spy(username, context)

    return None


def totah_sheli_end_poll(context):
    job = context.job

    poll = context.bot.stop_poll(job.context['poll_message'].chat_id, job.context['poll_message'].message_id)
    if poll is not None:
        podonki = poll.options[0].voter_count + poll.options[1].voter_count
        bratva = job.context['user_count']
        if podonki > bratva/2:
            apply_totah_level(DEFAULT_TOTAH_LEVEL, job.context['user'], job.context['poll_message'], context, additional_text='Tak решили {0} подонков из {1}!'.format(podonki, bratva))
    else:
        job.context['poll_message'].reply_text('Демократии конец, и ты сосёшь хуец!')


def totah_sheli_command(update, context):
    mi_totah_shel_aba = get_totah_shel_aba(update.message, context)

    if mi_totah_shel_aba is None:
        update.message.reply_text("Я не понял, а кто тотах то?")
        return

    logger.debug('totah_sheli: user: "%s"', mi_totah_shel_aba)

    question = "Заебались ли вы от " + mir_dolzhen_znat_geroev(mi_totah_shel_aba) + "?"
    poll_message = context.bot.send_poll(update.message.chat_id, question, ["Канешна!", "Давно пора!"])
    if poll_message is not None:
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        due = datetime.datetime.utcnow() + datetime.timedelta(minutes=POLL_TIME)
        new_job = context.job_queue.run_once(totah_sheli_end_poll, due, context={'poll_message': poll_message, 'user': mi_totah_shel_aba, 'user_count': beria_how_many_spies(context)})
        context.chat_data['job'] = new_job


def totah_sheli_poll_update(update, context):
    # no chat_id or chat_data available here
    return None


def get_totah_permissions():
    return ChatPermissions(can_send_messages=False,
                           can_change_info=False,
                           can_invite_users=False,
                           can_send_media_messages=False,
                           can_send_polls=False,
                           can_send_other_messages=False,
                           can_add_web_page_previews=False,
                           can_pin_messages=False)


def mir_dolzhen_znat_geroev(user):
    name = user.first_name
    if user.username is not None:
        name += ' "' + user.username + '"'
    if user.last_name is not None:
        name += " " + user.last_name
    return name


def apply_totah_level(totah_level, user, message, context, additional_text=None):
    if totah_level < 1:
        totah_level = DEFAULT_TOTAH_LEVEL

    until = datetime.datetime.utcnow() + datetime.timedelta(minutes=totah_level)
    permissions = get_totah_permissions()
    name = mir_dolzhen_znat_geroev(user)
    text = '{0} будет тотахом аж на {1}!'.format(name, totah_level)
    if additional_text is not None:
        text += "\n" + additional_text
    message.reply_text(text)
    logger.debug('restrict: chat_id: "%s" user: "%s"', message.chat_id, user.id)
    context.bot.restrict_chat_member(message.chat_id, user.id, permissions, until_date=until)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(sys.argv[1], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("totah", totah_command))
    dp.add_handler(CommandHandler("totahsheli", totah_sheli_command))

    # handle messages
    dp.add_handler(PollHandler(totah_sheli_poll_update))
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
