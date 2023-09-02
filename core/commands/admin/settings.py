#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.decorators import check_is_admin, delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


@on_update(
    filters=filters.command(["settings"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@check_is_admin
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await update.lang

    m = await message(
        update,
        context,
        lang["SETTINGS"]["SETTINGS_MODE_SELECTION"].format_map(Text()),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Classic", callback_data="settings"),
                    InlineKeyboardButton("Modern", callback_data="settings|modern"),
                ],
            ]
        ),
    )
    Session.last_settings[update.effective_chat.id] = m.message_id
