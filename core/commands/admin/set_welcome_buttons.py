#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


async def get_welcome_buttons(chat_id: int):
    buttons = json.loads((await Groups.get(id_group=chat_id)).welcome_buttons)
    result = []

    for i, row in enumerate(buttons):
        tmp = []
        for y, column in enumerate(row):
            tmp.append(
                InlineKeyboardButton(
                    column["name"], callback_data=f"welcome|buttons|del|{i}|{y}"
                )
            )

        if len(row) < Session.config.MAX_KEYBOARD_COLUMN:
            tmp.append(
                InlineKeyboardButton(
                    "{PLUS}".format_map(Text()),
                    callback_data=f"welcome|buttons|add|{i}",
                )
            )

        result.append(tmp)

    if len(result) < Session.config.MAX_KEYBOARD_ROW:
        result.append(
            [
                InlineKeyboardButton(
                    "{PLUS}".format_map(Text()), callback_data="welcome|buttons|add"
                )
            ]
        )

    return InlineKeyboardMarkup(result)


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
