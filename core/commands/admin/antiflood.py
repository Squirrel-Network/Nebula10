#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.decorators import check_role, delete_command, on_update
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang
from core.database.models import Groups
from core.utilities.menu import build_menu


@on_update()
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def set_antiflood(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    data = await Groups.get(id_group=update.effective_chat.id)

    buttons = [
        InlineKeyboardButton("MESSAGES", callback_data="XX"),
        InlineKeyboardButton(
            "{MINUS}".format_map(Text()), callback_data="antiflood|set|messages|minus"
        ),
        InlineKeyboardButton(
            data.antiflood_max_messages, callback_data="antiflood|messages"
        ),
        InlineKeyboardButton(
            "{PLUS}".format_map(Text()), callback_data="antiflood|set|messages|plus"
        ),
        InlineKeyboardButton("SECONDS", callback_data="XX"),
        InlineKeyboardButton(
            "{MINUS}".format_map(Text()), callback_data="antiflood|set|seconds|minus"
        ),
        InlineKeyboardButton(data.antiflood_seconds, callback_data="antiflood|seconds"),
        InlineKeyboardButton(
            "{PLUS}".format_map(Text()), callback_data="antiflood|set|seconds|plus"
        ),
    ]
    params = {"name": update.effective_chat.title, "chat_id": update.effective_chat.id}

    await message(
        update,
        context,
        lang["ANTIFLOOD_SETTING"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 4)),
    )
