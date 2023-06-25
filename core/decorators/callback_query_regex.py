#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import re
import typing

from telegram.ext import ContextTypes

from core.utilities.telegram_update import TelegramUpdate


def callback_query_regex(data: str):
    def decorator(func: typing.Callable):
        @functools.wraps(func)
        async def wrapper(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
            if any(re.findall(data, update.callback_query.data)):
                return await func(update, context)
            return

        return wrapper

    return decorator
