#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram import Update
from telegram.ext import ContextTypes

from core.utilities.telegram_update import TelegramUpdate


def on_update(priority: bool = False):
    def decorator(func: typing.Callable):
        func.priority = priority

        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            up = TelegramUpdate(
                **{
                    x: getattr(update, x, None)
                    for x in update.__slots__
                    if not x.startswith("_")
                }
            )

            return await func(up, context)

        return wrapper

    return decorator
