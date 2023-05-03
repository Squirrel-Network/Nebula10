#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import CallbackQueryHandler, CommandHandler

from core.commands.admin import say, settings
from core.commands.owner import server, superban, test
from core.commands.user import help, io, start
from core.utilities.functions import close_menu


def admin_command(bot):
    bot(CommandHandler("say", say.init))
    bot(CommandHandler("settings", settings.init))

def owner_command(bot):
    bot(CommandHandler("test", test.command_test))
    bot(CommandHandler("server", server.init))
    bot(CommandHandler("s", superban.init))
    bot(CommandHandler("ms", superban.multi_superban))
    bot(CommandHandler("us", superban.remove_superban_via_id))
    
    # CallbackQuery Handler
    bot(CallbackQueryHandler(close_menu, pattern='closeMenu'))
    bot(CallbackQueryHandler(superban.update_superban, pattern='m'))
    bot(CallbackQueryHandler(superban.update_superban, pattern='removeSuperban'))


def user_command(bot):
    bot(CommandHandler("start", start.init))
    bot(CommandHandler("io", io.init))
    bot(CommandHandler("help", help.init))
