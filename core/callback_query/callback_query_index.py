#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CallbackQueryHandler

from core.callback_query import admin, user
from core.callback_query.owner import owner, superban


def owner_callback(application: Application):
    application.add_handler(CallbackQueryHandler(superban.init, r"^superban\|"))
    application.add_handler(CallbackQueryHandler(owner.init, r"^owner\|remove$"))


def admin_callback(application: Application):
    application.add_handler(CallbackQueryHandler(admin.settings.init, r"^settings\|"))
    application.add_handler(CallbackQueryHandler(admin.languages.init, r"^lang$"))
    application.add_handler(
        CallbackQueryHandler(admin.languages.change_lang, r"^lang\|([a-zA-Z]+)$")
    )

    # Warn
    application.add_handler(CallbackQueryHandler(admin.warn.warn_down, r"^warn\|down$"))
    application.add_handler(CallbackQueryHandler(admin.warn.warn_up, r"^warn\|up$"))
    application.add_handler(
        CallbackQueryHandler(admin.warn.warn_del, r"^warn\|remove$")
    )
    application.add_handler(
        CallbackQueryHandler(admin.warn.set_max_warn_cb, r"^warn\|set\|(\d+)$")
    )

    # antiflood
    application.add_handler(
        CallbackQueryHandler(
            admin.antiflood.set_antiflood_minus_cb,
            r"^antiflood\|set\|(messages|seconds)\|minus$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.antiflood.set_antiflood_plus_cb,
            r"^antiflood\|set\|(messages|seconds)\|plus$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.antiflood.set_antiflood_success, r"^antiflood\|success$"
        )
    )

    # antistorm
    application.add_handler(
        CallbackQueryHandler(
            admin.antistorm.set_antistorm_minus_cb,
            r"^antistorm\|set\|(users|seconds)\|minus$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.antistorm.set_antistorm_plus_cb,
            r"^antistorm\|set\|(users|seconds)\|plus$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.antistorm.set_antistorm_success, r"^antistorm\|success$"
        )
    )
    # Welcome button
    application.add_handler(
        CallbackQueryHandler(
            admin.set_welcome_buttons.del_welcome_buttons,
            r"^welcome\|buttons\|del\|\d\|\d$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.set_welcome_buttons.add_welcome_buttons,
            r"^welcome\|buttons\|add\|\d\|\d$",
        )
    )


def user_callback(application: Application):
    application.add_handler(CallbackQueryHandler(user.close.init, r"^close$"))
    application.add_handler(CallbackQueryHandler(user.rules.init, r"^rules\|open$"))
    application.add_handler(
        CallbackQueryHandler(user.report.init, r"^report\|resolved$")
    )
