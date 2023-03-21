#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.repository.group import GroupRepository
async def command_test(update,context):
    bot = context.bot
    chat = update.effective_chat.id
    row = GroupRepository().getById([chat])
    await bot.send_message(chat, "<code>{}</code>".format(row),parse_mode='HTML')