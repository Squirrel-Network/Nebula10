#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import (
    Application,
    ChatMemberHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from core.decorators import on_update
from core.handlers.chat_handlers import chat_status, welcome
from core.handlers.chat_handlers.chat_status import check_updates
from core.handlers.user_handlers import user_status
from core.utilities.telegram_update import TelegramUpdate


def core_handlers(application: Application):
    print("A")
    application.add_handler(
        ChatMemberHandler(welcome.new_member, ChatMemberHandler.CHAT_MEMBER),
        group=-100,
    )
    application.add_handler(MessageHandler(filters.ALL, group_handlers), group=-101)
    application.add_handler(
        ChatMemberHandler(welcome.welcome_bot, ChatMemberHandler.MY_CHAT_MEMBER),
        group=-102,
    )


@on_update
async def group_handlers(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        return

    await chat_status.status(update, context)
    await user_status.status(update, context)
    await check_updates(update, context)
