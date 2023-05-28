#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CallbackQueryHandler

from core.callback_query.admin import languages, settings
from core.callback_query.owner import owner, superban
from core.callback_query.user import close


def owner_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(superban.init)], group=1)
    application.add_handlers([CallbackQueryHandler(owner.init)], group=2)


def admin_callback(application: Application):
    application.add_handler(CallbackQueryHandler(settings.init), group=100)
    application.add_handler(CallbackQueryHandler(languages.init), group=101)
    application.add_handler(CallbackQueryHandler(languages.change_lang), group=102)


def user_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(close.init)], group=200)
