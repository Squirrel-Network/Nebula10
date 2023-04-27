#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core import decorators
from core.utilities.message import message
from core.utilities.entities import TelegramObjects
from core.database.repository.superban import SuperbanRepository

@decorators.private.init
@decorators.delete.init
async def init(update,context):
    user = TelegramObjects(update,context).user_object()
    nickname = "@"+ user.username
    superban = SuperbanRepository().getById(user.id)
    if superban:
        URL = "https://squirrel-network.online/knowhere/?q={}".format(user.id)
        msg = "ℹ️ == User Information ==  ℹ️\n\n<b>🆔 User id:</b> <code>{}</code>\n<b>👤 Nickname:</b> {}\n<b>🚷 Blacklist:</b> ✅\nLearn more about: {}".format(user.id, nickname or user.first_name,URL)
    else:
        msg = "ℹ️ == User Information ==  ℹ️\n\n<b>🆔 User id:</b> <code>{}</code>\n<b>👤 Nickname:</b> {}\n<b>🚷 Blacklist:</b> ❌".format(user.id, nickname or user.first_name)
    await message(update,context,msg)