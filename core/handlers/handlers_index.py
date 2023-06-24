#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from core.handlers.chat_handlers import chat_status, welcome
from core.handlers.chat_handlers.chat_status import check_updates
from core.handlers.user_handlers import user_status


def core_handlers(application: Application):
    application.add_handlers(
        [
            # MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member),
            # MessageHandler(filters.ALL, group_handlers),
        ]
    )


async def group_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_status.status(update, context)
    await user_status.status(update, context)
    await check_updates(update)
