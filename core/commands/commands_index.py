#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    filters,
)

from core.commands.admin import say, settings
from core.commands.owner import server, superban, test
from core.commands.user import help, io, start


def admin_command(application: Application):
    application.add_handlers(
        [
            CommandHandler("say", say.init),
            CommandHandler("settings", settings.init, filters=filters.ChatType.GROUPS),
        ]
    )


def owner_command(application: Application):
    application.add_handlers(
        [
            CommandHandler("test", test.command_test),
            CommandHandler("server", server.init),
            CommandHandler("s", superban.init),
            CommandHandler("ms", superban.multi_superban),
            CommandHandler("us", superban.remove_superban_via_id),
        ]
    )


def user_command(application: Application):
    application.add_handlers(
        [
            CommandHandler("start", start.init, filters=filters.ChatType.PRIVATE),
            CommandHandler("io", io.init, filters=filters.ChatType.PRIVATE),
            CommandHandler("help", help.init),
        ]
    )
