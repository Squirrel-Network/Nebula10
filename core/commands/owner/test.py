#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
async def command_test(update,context):
    bot = context.bot
    chat = update.effective_chat.id
    await bot.send_message(chat, "Ciao")