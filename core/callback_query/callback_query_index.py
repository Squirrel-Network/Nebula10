#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CallbackQueryHandler

from core.callback_query.admin import languages, settings
from core.callback_query.owner import owner, superban
from core.callback_query.user import close


def owner_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(superban.init)])
    application.add_handlers([CallbackQueryHandler(owner.init)])


def admin_callback(application: Application):
    application.add_handler(CallbackQueryHandler(settings.init))
    application.add_handler(CallbackQueryHandler(languages.init))
    application.add_handler(CallbackQueryHandler(languages.change_lang))


def user_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(close.init)])
