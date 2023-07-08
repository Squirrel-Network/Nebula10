#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import check_is_admin, check_role, delete_command, on_update
from core.utilities.enums import Role
from core.utilities.functions import get_keyboard_settings
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update()
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@check_is_admin
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    params = {
        "name": update.effective_chat.title,
        "id": update.effective_chat.id,
    }
    await message(
        update,
        context,
        (await get_lang(update))["MAIN_TEXT_SETTINGS"].format_map(Text(params)),
        reply_markup=await get_keyboard_settings(update.effective_chat.id),
    )
