#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CallbackQueryHandler

from core.callback_query import admin
from core.callback_query.owner import owner, superban
from core.callback_query.user import close


def owner_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(superban.init)])
    application.add_handlers([CallbackQueryHandler(owner.init)])


def admin_callback(application: Application):
    application.add_handler(CallbackQueryHandler(admin.settings.init))
    application.add_handler(CallbackQueryHandler(admin.languages.init))
    application.add_handler(CallbackQueryHandler(admin.languages.change_lang))

    # Warn
    application.add_handler(CallbackQueryHandler(admin.warn.warn_down))
    application.add_handler(CallbackQueryHandler(admin.warn.warn_up))
    application.add_handler(CallbackQueryHandler(admin.warn.warn_del))
    application.add_handler(CallbackQueryHandler(admin.warn.set_max_warn_cb))

    # antiflood
    application.add_handler(
        CallbackQueryHandler(admin.antiflood.set_antiflood_minus_cb)
    )
    application.add_handler(CallbackQueryHandler(admin.antiflood.set_antiflood_plus_cb))
    application.add_handler(CallbackQueryHandler(admin.antiflood.set_antiflood_success))


def user_callback(application: Application):
    application.add_handlers([CallbackQueryHandler(close.init)])
