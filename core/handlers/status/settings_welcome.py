#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.functions import validate_html
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


@on_update(
    True,
    filters.group
    & ~filters.reply
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.check_status("set_welcome_text")
    & filters.text,
)
async def set_welcome_text_status(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await update.lang
    key = f"{update.effective_user.id}-{update.effective_chat.id}"
    data = Session.status.pop(key)

    await context.bot.delete_message(update.effective_chat.id, data["message_id"])

    if not validate_html(update.effective_message.text):
        return await message(
            update,
            context,
            lang["SETTINGS"]["WELCOME"]["SETTINGS_WELCOME_TEXT_INVALID_HTML"],
        )

    await Groups.filter(id_group=update.effective_chat.id).update(
        welcome_text=update.effective_message.text
    )
    await message(
        update,
        context,
        lang["SETTINGS"]["WELCOME"]["SETTINGS_WELCOME_TEXT_DONE"].format_map(Text()),
    )
