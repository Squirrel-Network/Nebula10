#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.decorators import check_is_admin, delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang


@on_update(
    filters=filters.command(["settings"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@check_is_admin
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    buttons = [
        [
            InlineKeyboardButton("Classic", callback_data="settings|page|1"),
            InlineKeyboardButton("Modern", callback_data="settings|modern"),
        ],
    ]

    await message(
        update,
        context,
        lang["SETTINGS_MODE_SELECTION"],
        reply_markup=InlineKeyboardMarkup(buttons),
    )
