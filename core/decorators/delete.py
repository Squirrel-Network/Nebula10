#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram.ext import ContextTypes

from core.utilities.telegram_update import TelegramUpdate


def delete_command(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text and update.message.text.startswith("/"):
            await update.message.delete()

        return await func(update, context)

    return wrapper
