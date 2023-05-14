#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CallbackQueryHandler

from core.callback_query.user import close
from core.callback_query.owner import superban
from core.callback_query.admin import settings, languages


def owner_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(superban.init, "superban|")])


def admin_callback(application: Application):
    application.add_handler(CallbackQueryHandler(settings.init, "settings|"))
    application.add_handler(CallbackQueryHandler(languages.init, "^lang$"))
    application.add_handler(CallbackQueryHandler(languages.change_lang, "lang|"))


def user_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(close.init, "close")])
