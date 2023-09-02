#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram.ext import ContextTypes

from config import Session
from core.utilities.telegram_update import TelegramUpdate


def check_settings(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if (
            not (v := Session.last_settings.get(update.effective_chat.id))
            or v != update.effective_message.message_id
        ):
            await update.effective_message.delete()
            return
        return await func(update, context)

    return wrapper
