#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

async def status(update, context):
    bot = context.bot
    chat = update.effective_chat.id
    print(update)
    await bot.send_message(chat, "test")