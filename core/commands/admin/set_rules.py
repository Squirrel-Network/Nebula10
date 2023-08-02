#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang


@on_update(
    filters=filters.command(["setrules"])
    & filters.group
    & ~filters.reply
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
)
@delete_command
async def set_rules(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    text = update.effective_message.text.split(maxsplit=1)

    if len(text) == 1:
        return await message(update, context, lang["SET_RULES_ERROR"])

    await Groups.filter(id_group=update.effective_chat.id).update(rules_text=text[1])
    await message(update, context, lang["SET_RULES_SUCCESS"])
