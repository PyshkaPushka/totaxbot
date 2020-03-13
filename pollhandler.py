from telegram.ext import Handler
from telegram import Update


class PollHandler(Handler):

    def __init__(self, callback):
        super(PollHandler, self).__init__(callback)

    def check_update(self, update):
        return isinstance(update, Update) and update.poll

    def collect_additional_context(self, context, update, dispatcher, check_result):
        if isinstance(check_result, dict):
            context.update(check_result)