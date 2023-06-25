#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes

from core.utilities.telegram_update import TelegramUpdate


def check_is_admin(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        chat_permission = await context.bot.get_chat_member(chat_id, context.bot.id)

        if not chat_permission.status == ChatMemberStatus.ADMINISTRATOR:
            await update.effective_message.reply_text("I'm not admin!")
            return

        return await func(update, context)

    return wrapper
