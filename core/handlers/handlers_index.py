#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, ChatMemberHandler, ContextTypes, MessageHandler

from core.decorators import on_update
from core.handlers import antiflood, antistorm, error
from core.handlers.chat_handlers import chat_status, welcome
from core.handlers.user_handlers import user_status
from core.utilities.telegram_update import TelegramUpdate


def core_handlers(application: Application):
    application.add_handler(MessageHandler(None, antiflood.init))
    application.add_handler(MessageHandler(None, antistorm.init))
    application.add_handler(
        ChatMemberHandler(welcome.new_member, ChatMemberHandler.CHAT_MEMBER)
    )
    application.add_handler(MessageHandler(None, group_handlers))
    application.add_handler(MessageHandler(None, chat_status.new_chat_title_handler))
    application.add_handler(
        MessageHandler(
            None,
            chat_status.new_chat_photo_handler,
        )
    )
    application.add_handler(
        ChatMemberHandler(welcome.welcome_bot, ChatMemberHandler.MY_CHAT_MEMBER)
    )
    application.add_handler(
        MessageHandler(
            None,
            chat_status.check_updates,
        )
    )
    application.add_error_handler(error.init)


@on_update(True)
async def group_handlers(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        return

    await user_status.status(update, context)
