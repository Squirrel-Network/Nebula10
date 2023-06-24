#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.database.models import SuperbanTable
from core.decorators import delete_command
from core.utilities.message import message
from core.utilities.text import Text
from languages import get_lang


@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    user = update.effective_message.from_user
    params = {
        "id": user.id,
        "name": f"@{user.username}" if user.username else user.name,
    }

    msg = lang["USER_INFORMATION"].format_map(Text(params))

    if await SuperbanTable.exists(user_id=user.id):
        params["url"] = f"https://squirrel-network.online/knowhere/?q={user.id}"
        msg = lang["USER_INFORMATION_SUPERBAN"].format_map(Text(params))

    await message(update, context, msg)
