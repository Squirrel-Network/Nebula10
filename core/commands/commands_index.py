#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, CommandHandler, filters

from core.commands import admin, owner, user


def admin_command(application: Application):
    application.add_handler(
        CommandHandler("filters", admin.filters.init, filters=filters.ChatType.GROUPS),
        group=1,
    )
    application.add_handler(CommandHandler("say", admin.say.init), group=2)
    application.add_handler(
        CommandHandler(
            "settings", admin.settings.init, filters=filters.ChatType.GROUPS
        ),
        group=3,
    )
    application.add_handler(CommandHandler("usearch", admin.usearch.init), group=4)


def owner_command(application: Application):
    application.add_handler(CommandHandler("test", owner.test.command_test), group=100)
    application.add_handler(CommandHandler("server", owner.server.init), group=101)
    application.add_handler(CommandHandler("bl", owner.superban.init), group=102)
    application.add_handler(
        CommandHandler("mbl", owner.superban.multi_superban), group=103
    )
    application.add_handler(
        CommandHandler("ubl", owner.superban.remove_superban_via_id), group=104
    )
    application.add_handler(CommandHandler("owner", owner.add_owner.init), group=105)


def user_command(application: Application):
    application.add_handler(
        CommandHandler("start", user.start.init, filters=filters.ChatType.PRIVATE),
        group=200,
    )
    application.add_handler(
        CommandHandler("io", user.io.init, filters=filters.ChatType.PRIVATE), group=201
    )
    application.add_handler(CommandHandler("help", user.help_command.init), group=202)
