#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import CallbackQueryHandler as CQH
from telegram.ext import CommandHandler as CMH
from telegram.ext import ChatMemberHandler

from core.commands import admin, owner, user
from core.utilities.functions import close_menu


def admin_command(bot):
    bot(CMH("say", admin.say.init))
    bot(CMH("settings", admin.settings.init))

def owner_command(bot):
    bot(CMH("test", owner.test.command_test))
    bot(CMH("server", owner.server.init))
    bot(CMH("s", owner.superban.init))
    bot(CMH("ms", owner.superban.multi_superban))
    bot(CMH("us", owner.superban.remove_superban_via_id))
    #############################
    ### CallbackQuery Handler ###
    #############################
    bot(CQH(close_menu, pattern='closeMenu'))
    bot(CQH(owner.superban.update_superban, pattern='m'))
    bot(CQH(owner.superban.update_superban, pattern='removeSuperban'))


def user_command(bot):
    bot(CMH("start", user.start.init))
    bot(CMH("io", user.io.init))
    bot(CMH("help", user.help.init))
