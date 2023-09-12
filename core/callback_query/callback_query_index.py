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
    # Settings - mode
    application.add_handler(
        CallbackQueryHandler(admin.settings.settings, r"^settings$")
    )
    application.add_handler(
        CallbackQueryHandler(admin.settings.settings_modern, r"^settings\|modern$")
    )

    # Settings - antiflood
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_antiflood.settings_antiflood, r"^settings\|antiflood$"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_antiflood.settings_antiflood_state_cb,
            r"^settings\|antiflood\|state$",
        )
    )

    # Settings - antistorm
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_antistorm.settings_antistorm, r"^settings\|antistorm$"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_antistorm.settings_antistorm_state_cb,
            r"^settings\|antistorm\|state$",
        )
    )

    # Settings - captcha
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_captcha.settings_captcha, r"^settings\|captcha$"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_captcha.settings_captcha_state_cb,
            r"^settings\|captcha\|state$",
        )
    )

    # Settings - chat block
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_chat_block.settings_chat_block, r"^settings\|chat_block$"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_chat_block.settings_chat_block_blocks,
            r"^settings\|chat_block\|blocks$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_chat_block.settings_chat_block_blocks_change,
            r"^settings\|chat_block\|blocks\|([a-zA-Z_-]+)$",
        )
    )

    # Settings - filters
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_filters.settings_filters, r"^settings\|filters$"
        )
    )

    # Settings - night
    application.add_handler(
        CallbackQueryHandler(admin.settings_night.settings_night, r"^settings\|night$")
    )

    # Settings - rules
    application.add_handler(
        CallbackQueryHandler(admin.settings_rules.settings_rules, r"^settings\|rules$")
    )

    # Settings - welcome
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_welcome.settings_welcome, r"^settings\|welcome$"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_welcome.settings_welcome_state_cb,
            r"^settings\|welcome\|state$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_welcome.settings_welcome_see_message_cb,
            r"^settings\|welcome\|see_message$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            admin.settings_welcome.settings_welcome_set_message_cb,
            r"^settings\|welcome\|set_message$",
        )
    )

    # Lang
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

    # Antiflood
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

    # Antistorm
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
            admin.set_welcome_buttons.del_welcome_buttons_confirm,
            r"^welcome\|buttons\|del\|confim\|\d\|\d$",
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
    application.add_handler(
        CallbackQueryHandler(user.captcha.init, r"^captcha\|\d+\|\d\|\d\|\d+$")
    )
