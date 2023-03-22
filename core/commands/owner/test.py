#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

#from core.database.repository.group import GroupRepository
#from core.utilities.message import message
from core.utilities.entities import TelegramObjects


async def command_test(update,context):
    #bot = context.bot
    #chat = update.effective_chat.id
    #get_chat = await bot.get_chat(chat_id=chat)
    #get_chat = TelegramObjects(update,context).chat_status_object()
    #get_chat = get_status_chat(update,context)
    get_chat = TelegramObjects(update,context).chat_object()

    #print(chat)
    print(get_chat)

    #row = GroupRepository().getById([chat])
    #await message(update,context,"<code>{}</code>".format(get),type="private")