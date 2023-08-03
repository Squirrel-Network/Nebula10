#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.functions import get_welcome_buttons
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang


@on_update(
    filters=filters.command(["welcomebuttons"])
    & filters.group
    & ~filters.reply
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
)
@delete_command
async def set_welcome_buttons(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)

    await message(
        update,
        context,
        lang["SET_WELCOME_BUTTONS"],
        reply_markup=await get_welcome_buttons(update.effective_chat.id),
    )
