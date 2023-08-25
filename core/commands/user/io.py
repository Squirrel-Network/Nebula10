#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.database.models import SuperbanTable
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.command(["io"]) & filters.private)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    user = update.effective_message.from_user
    params = {
        "id": user.id,
        "name": f"@{user.username}" if user.username else f"<>{user.name}</>",
    }

    msg = lang["USER_INFORMATION"].format_map(Text(params))

    if await SuperbanTable.exists(user_id=user.id):
        params["url"] = f"https://squirrel-network.online/knowhere/?q={user.id}"
        msg = lang["USER_INFORMATION_SUPERBAN"].format_map(Text(params))

    await message(update, context, msg)
