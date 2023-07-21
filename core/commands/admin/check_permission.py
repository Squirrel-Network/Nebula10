#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang

PERMISSION_CHECK = (
    "can_delete_messages",
    "can_restrict_members",
    "can_pin_messages",
)


@on_update(
    filters=filters.command(["check"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    permission = await context.bot.get_chat_member(
        update.effective_chat.id, context.bot.id
    )

    if not all([getattr(permission, x, False) for x in PERMISSION_CHECK]):
        return await message(update, context, lang["PERM_MSG_ERROR"].format_map(Text()))

    await message(update, context, lang["PERM_MSG_OK"].format_map(Text()))
