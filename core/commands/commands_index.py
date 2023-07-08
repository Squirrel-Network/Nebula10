#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CommandHandler, filters

from core.commands import admin, owner, user
from core.utilities.filters import REPLY_TEXT


def admin_command(application: Application):
    application.add_handler(
        CommandHandler("filters", admin.filters.init, filters=filters.ChatType.GROUPS)
    )
    application.add_handler(CommandHandler("say", admin.say.init))
    application.add_handler(
        CommandHandler("settings", admin.settings.init, filters=filters.ChatType.GROUPS)
    )
    application.add_handler(CommandHandler("usearch", admin.usearch.init))
    application.add_handler(CommandHandler("ban", admin.ban.init, ~filters.REPLY))
    application.add_handler(CommandHandler("ban", admin.ban.init_reply, filters.REPLY))
    application.add_handler(
        CommandHandler("setban", admin.ban.set_ban_message, ~filters.REPLY)
    )
    application.add_handler(
        CommandHandler(
            "setban", admin.ban.set_ban_message_reply, filters.REPLY & REPLY_TEXT
        )
    )
    application.add_handler(
        CommandHandler("unban", admin.unban.init_reply, filters.REPLY)
    )
    application.add_handler(CommandHandler("check", admin.check_permission.init))


def owner_command(application: Application):
    application.add_handler(CommandHandler("test", owner.test.command_test))
    application.add_handler(CommandHandler("server", owner.server.init))
    application.add_handler(CommandHandler("bl", owner.superban.init))
    application.add_handler(CommandHandler("mbl", owner.superban.multi_superban))
    application.add_handler(
        CommandHandler("ubl", owner.superban.remove_superban_via_id)
    )
    application.add_handler(CommandHandler("owner", owner.add_owner.init))


def user_command(application: Application):
    application.add_handler(
        CommandHandler("start", user.start.init, filters=filters.ChatType.PRIVATE)
    )
    application.add_handler(
        CommandHandler("io", user.io.init, filters=filters.ChatType.PRIVATE)
    )
    application.add_handler(CommandHandler("help", user.help_command.init))
