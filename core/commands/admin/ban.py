#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

async def ban_command(update,context):
    print("dentro ban command")
    bot = context.bot
    chat = update.effective_chat.id
    await bot.send_message(chat, "Test Ban")