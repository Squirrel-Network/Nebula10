#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes
from telegram.constants import ChatType

from core.database.models import Community
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(
    filters=filters.command(["community"])
    & filters.check_role(Role.OWNER)
    & filters.group
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    chat = update.effective_chat

    if not chat.type == ChatType.SUPERGROUP or not chat.username:
        return await message(update, context, lang["ADD_COMMUNITY_ERROR"])

    _, status = await Community.update_or_create(
        tg_group_id=chat.id,
        defaults={
            "tg_group_name": chat.title,
            "tg_group_link": f"https://t.me/{chat.username}",
            "type": chat.type,
        },
    )

    if status:
        params = {"id": chat.id}
        await message(update, context, lang["ADD_COMMUNITY"].format_map(Text(params)))
    else:
        await message(update, context, lang["ADD_COMMUNITY_UPDATE"])
