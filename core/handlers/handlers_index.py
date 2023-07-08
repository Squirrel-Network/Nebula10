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
from core.handlers.user_handlers import user_status
from core.utilities.telegram_update import TelegramUpdate


def core_handlers(application: Application):
    application.add_handler(
        ChatMemberHandler(welcome.new_member, ChatMemberHandler.CHAT_MEMBER)
    )
    application.add_handler(MessageHandler(filters.ALL, group_handlers))
    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_TITLE, chat_status.new_chat_title_handler
        )
    )
    application.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_PHOTO,
            chat_status.new_chat_photo_handler,
        )
    )
    application.add_handler(
        ChatMemberHandler(welcome.welcome_bot, ChatMemberHandler.MY_CHAT_MEMBER)
    )
    application.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS & ~filters.StatusUpdate.LEFT_CHAT_MEMBER,
            chat_status.check_updates,
        )
    )


@on_update(True)
async def group_handlers(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        return

    await user_status.status(update, context)
