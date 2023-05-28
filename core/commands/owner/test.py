#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

# from core.database.repository.group import GroupRepository
# from core.utilities.message import message


async def command_test(update, context):
    bot = context.bot
    chat = update.effective_chat.id
    user = update.effective_user.id
    print(chat)
    print(user)
    # get_chat = await bot.get_chat(chat_id=chat)
    # get_chat = TelegramObjects(update,context).chat_status_object()
    # get_chat = get_status_chat(update,context)
    # get_chat = TelegramObjects(update,context).chat_object()
    # stat = context.bot.get_chat_member(update.message.chat_id, update.effective_user['id'])['status']
    stat = await bot.get_chat_member(chat, user)
    test = stat.status

    # print(chat)
    print(test)

    # row = GroupRepository().getById([chat])
    # await message(update,context,"<code>{}</code>".format(get),type="private")
