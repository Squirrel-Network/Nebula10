#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram import Update
from telegram.ext import ContextTypes

from core.utilities.telegram_update import TelegramUpdate


def on_update(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        u = TelegramUpdate(
            update,
            update.effective_chat,
            update.effective_user,
            update.message.reply_to_message.from_user
            if update.message.reply_to_message
            else None,
        )

        return await func(u, context)

    return wrapper
