#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram import Update
from telegram.ext import ContextTypes


def delete_command(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text and update.message.text.startswith("/"):
            await context.bot.delete_message(
                update.effective_message.chat_id, update.message.message_id
            )

        return await func(update, context)
    return wrapper
