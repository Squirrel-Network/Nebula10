#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

async def new_member(update, context):
    bot = context.bot
    chat = update.effective_chat.id
    for member in update.message.new_chat_members:
        print(member)
        await bot.send_message(chat, "Welcome {} in {}".format(member.first_name, update.message.chat.title))