#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CommandHandler, filters

from core.commands import admin, owner, user


def admin_command(application: Application):
    application.add_handlers(
        [
            CommandHandler(
                "filters", admin.filters.init, filters=filters.ChatType.GROUPS
            ),
            CommandHandler("say", admin.say.init),
            CommandHandler(
                "settings", admin.settings.init, filters=filters.ChatType.GROUPS
            ),
        ]
    )


def owner_command(application: Application):
    application.add_handlers(
        [
            CommandHandler("test", owner.test.command_test),
            CommandHandler("testdue", owner.test.command_test_due),
            CommandHandler("server", owner.server.init),
            CommandHandler("bl", owner.superban.init),
            CommandHandler("mbl", owner.superban.multi_superban),
            CommandHandler("ubl", owner.superban.remove_superban_via_id),
            CommandHandler("owner", owner.add_owner.init),
        ]
    )


def user_command(application: Application):
    application.add_handlers(
        [
            CommandHandler("start", user.start.init, filters=filters.ChatType.PRIVATE),
            CommandHandler("io", user.io.init, filters=filters.ChatType.PRIVATE),
            CommandHandler("help", user.help_command.init),
        ]
    )
