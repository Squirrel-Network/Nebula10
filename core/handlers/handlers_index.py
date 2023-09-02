#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, ChatMemberHandler, MessageHandler

from core.handlers import error
from core.handlers.chat_handlers import (
    antiflood,
    antistorm,
    chat_status,
    filters,
    welcome,
)
from core.handlers.user_handlers import automatic_handler
from core.handlers import status


def core_handlers(application: Application):
    application.add_handler(MessageHandler(None, chat_status.change_group_info))
    application.add_handler(
        ChatMemberHandler(
            chat_status.change_group_info, ChatMemberHandler.ANY_CHAT_MEMBER
        )
    )
    application.add_handler(
        MessageHandler(
            None,
            chat_status.check_updates,
        )
    )
    application.add_handler(
        MessageHandler(
            None,
            automatic_handler.status,
        )
    )
    application.add_handler(MessageHandler(None, antiflood.init))
    application.add_handler(
        ChatMemberHandler(antistorm.init, ChatMemberHandler.CHAT_MEMBER)
    )
    application.add_handler(
        ChatMemberHandler(welcome.new_member, ChatMemberHandler.CHAT_MEMBER)
    )
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
    application.add_handler(MessageHandler(None, filters.filters_chat))
    application.add_handler(
        MessageHandler(None, status.settings_welcome.set_welcome_text_status)
    )
    application.add_error_handler(error.init)
