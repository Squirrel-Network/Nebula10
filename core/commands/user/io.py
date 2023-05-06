#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes
from core.utilities.message import message
from core.database.repository.superban import SuperbanRepository
from core.decorators import delete_command
from core.utilities.text import Text
from languages import get_lang


@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    user = update.effective_message.from_user
    params = {
        "id": user.id,
        "name": f"@{user.username}" if user.username else user.name,
    }

    msg = lang["USER_INFORMATION"].format_map(Text(params))
    with SuperbanRepository() as db:
        superban = db.get_by_id(user.id)

    if superban:
        params["url"] = f"https://squirrel-network.online/knowhere/?q={user.id}"
        msg = lang["USER_INFORMATION_SUPERBAN"].format_map(Text(params))

    await message(update, context, msg)
