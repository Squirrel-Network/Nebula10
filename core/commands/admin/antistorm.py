#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(
    filters=filters.command(["setantistorm"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def set_antistorm(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    data = await Groups.get(id_group=update.effective_chat.id)

    buttons = [
        InlineKeyboardButton("USERS", callback_data="XX"),
        InlineKeyboardButton(
            "{MINUS}".format_map(Text()), callback_data="antistorm|set|users|minus"
        ),
        InlineKeyboardButton(data.antistorm_max_users, callback_data="antistorm|users"),
        InlineKeyboardButton(
            "{PLUS}".format_map(Text()), callback_data="antistorm|set|users|plus"
        ),
        InlineKeyboardButton("SECONDS", callback_data="XX"),
        InlineKeyboardButton(
            "{MINUS}".format_map(Text()), callback_data="antistorm|set|seconds|minus"
        ),
        InlineKeyboardButton(data.antistorm_seconds, callback_data="antistorm|seconds"),
        InlineKeyboardButton(
            "{PLUS}".format_map(Text()), callback_data="antistorm|set|seconds|plus"
        ),
        InlineKeyboardButton(
            "{CHECK_MARK_BUTTON}".format_map(Text()), callback_data="antistorm|success"
        ),
    ]
    params = {
        "name": f"<>{update.effective_chat.title}</>",
        "chat_id": update.effective_chat.id,
    }

    await message(
        update,
        context,
        lang["ANTISTORM_SETTING"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 4)),
    )
