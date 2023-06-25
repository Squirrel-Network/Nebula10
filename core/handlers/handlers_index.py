#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
    ChatMemberHandler,
)

from core.handlers.chat_handlers import chat_status, welcome
from core.handlers.chat_handlers.chat_status import check_updates
from core.handlers.user_handlers import user_status


def core_handlers(application: Application):
    application.add_handler(
        ChatMemberHandler(welcome.new_member, ChatMemberHandler.CHAT_MEMBER),
        group=-100,
    )
    application.add_handler(MessageHandler(filters.ALL, group_handlers), group=-101)
    application.add_handler(
        ChatMemberHandler(welcome.welcome_bot, ChatMemberHandler.MY_CHAT_MEMBER),
        group=-102,
    )


async def group_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_status.status(update, context)
    await user_status.status(update, context)
    await check_updates(update, context)
