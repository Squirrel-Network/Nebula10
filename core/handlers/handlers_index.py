#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, ChatMemberHandler, MessageHandler

from core.handlers import antiflood, antistorm, error
from core.handlers.chat_handlers import chat_status, welcome
from core.handlers.user_handlers import user_status


def core_handlers(application: Application):
    application.add_handler(MessageHandler(None, chat_status.change_group_info))
    application.add_handler(
        MessageHandler(
            None,
            chat_status.check_updates,
        )
    )
    application.add_handler(
        MessageHandler(
            None,
            user_status.status,
        )
    )
    application.add_handler(MessageHandler(None, antiflood.init))
    application.add_handler(MessageHandler(None, antistorm.init))
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
    application.add_error_handler(error.init)
