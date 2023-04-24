#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from functools import wraps

def init(func):
    @wraps(func)
    async def wrapped(update, context):
        bot = context.bot
        if update.message.text is not None:
            if update.message.text.startswith("/"):
                await bot.delete_message(update.effective_message.chat_id, update.message.message_id)
            else:
                print("AAA")
        return await func(update, context)
    return wrapped