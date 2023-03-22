#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import CommandHandler as CMH
from core.commands import admin,owner,user

def admin_command(bot):
    bot(CMH("ban",admin.ban.ban_command))
    bot(CMH("say", admin.say.init))

def owner_command(bot):
    bot(CMH("test", owner.test.command_test))
    bot(CMH("server", owner.server.init))

def user_command(bot):
    bot(CMH("start", user.start.start))