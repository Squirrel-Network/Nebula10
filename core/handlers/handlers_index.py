#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core import handlers
from telegram.ext import MessageHandler, filters


def core_handlers(bot):
    bot(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handlers.chat_handlers.welcome.new_member))
    bot(MessageHandler(filters.ALL, group_handlers))

async def group_handlers(update, context):
    await handlers.chat_handlers.chat_status.status(update,context)