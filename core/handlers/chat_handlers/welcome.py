#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core.utilities.entities import TelegramObjects
from core.utilities.functions import save_group
from core.database.repository.group import GroupRepository

async def new_member(update, context):
    bot = context.bot
    chat = TelegramObjects(update, context).chat_object()
    for member in update.message.new_chat_members:
        row = GroupRepository().getById(chat.id)
        print(member)
        if row:
            print("UPDATE GROUP")
        else:
            save_group(update.effective_chat.id, update.effective_chat.title)
        await bot.send_message(chat.id, "Welcome {} in {}".format(member.first_name, update.message.chat.title))
