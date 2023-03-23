#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import (CommandHandler as CMH,CallbackQueryHandler as CQH)
from core.commands import admin,owner,user
from core.utilities.functions import close_menu

def admin_command(bot):
    bot(CMH("ban",admin.ban.ban_command))
    bot(CMH("say", admin.say.init))

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
    bot(CMH("start", user.start.start))