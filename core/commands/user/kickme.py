#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.functions import kick_user
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(
    filters=filters.command(["kickme"])
    & filters.group
    & ~filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
)
@delete_command
async def kickme_command(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    user_id = update.effective_user.id
    img = "https://i.imgur.com/CKU9Y75.png"
    params = {"id": user_id}

    await kick_user(update.effective_chat.id, user_id, context)
    await message(
        update,
        context,
        lang["KICK_ME_COMMAND"].format_map(Text(params)),
        "HTML",
        "photo",
        None,
        img,
    )
