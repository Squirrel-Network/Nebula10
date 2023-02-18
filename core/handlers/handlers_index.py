#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import MessageHandler, filters
from core.handlers import chat_handlers

def core_handlers(bot):
    bot(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, chat_handlers.welcome.new_member))