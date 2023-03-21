#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.repository.group import GroupRepository
from core.utilities.message import message
async def command_test(update,context):
    chat = update.effective_chat.id
    row = GroupRepository().getById([chat])
    await message(update,context,"<code>{}</code>".format(row),type="private")