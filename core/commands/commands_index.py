#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import CommandHandler as CMH
from core.commands import admin,user,owner

def user_command(bot):
    bot(CMH("start", user.start.start))

def admin_command(bot):
    pass

def owner_command(bot):
    bot(CMH("test", owner.test))