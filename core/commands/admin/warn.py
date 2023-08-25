#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.database.models import Groups, GroupUsers
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang

WARN_USER_BUTTON = [
    InlineKeyboardButton("{MINUS} 1".format_map(Text()), callback_data="warn|down"),
    InlineKeyboardButton("{PLUS} 1".format_map(Text()), callback_data="warn|up"),
    InlineKeyboardButton(
        "{WASTEBASKET} Rimuovi".format_map(Text()), callback_data="warn|remove"
    ),
]
SETTING_BUTTON = (
    (2, "KEYCAP_DIGIT_TWO"),
    (3, "KEYCAP_DIGIT_THREE"),
    (4, "KEYCAP_DIGIT_FOUR"),
    (5, "KEYCAP_DIGIT_FIVE"),
    (6, "KEYCAP_DIGIT_SIX"),
    (7, "KEYCAP_DIGIT_SEVEN"),
    (8, "KEYCAP_DIGIT_EIGHT"),
    (9, "KEYCAP_DIGIT_NINE"),
    (10, "KEYCAP_10"),
)


@on_update(
    filters=filters.command(["warn"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.reply
    & filters.group
)
@delete_command
async def init_reply(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    reply = update.effective_message.reply_to_message.from_user
    reason = v[1] if len(v := update.effective_message.text.split()) > 1 else None

    data = await Groups.get(id_group=update.effective_chat.id)
    user = await GroupUsers.get(tg_id=reply.id, tg_group_id=update.effective_chat.id)
    max_warn = data.max_warn
    user_warn = user.warn_count

    if user_warn == max_warn:
        await context.bot.ban_chat_member(update.effective_chat.id, reply.id)
        params = {
            "username": reply.username,
            "title": f"<>{update.effective_chat.title}</>",
        }

        return await update.message.reply_to_message.reply_text(
            lang["WARN_USER_MAX"].format_map(Text(params))
        )

    params = {
        "name": f"<>{reply.first_name}</>",
        "count": user_warn + 1,
        "max_warn": max_warn,
        "group_name": f"<>{update.effective_chat.title}</>",
        "group_id": update.effective_chat.id,
    }
    msg = lang["WARN_USER"].format_map(Text(params))

    if reason:
        params["reason"] = reason
        msg = lang["WARN_USER_REASON"].format_map(Text(params))

    await GroupUsers.filter(
        tg_id=reply.id, tg_group_id=update.effective_chat.id
    ).update(warn_count=user_warn + 1)

    await update.message.reply_to_message.reply_text(
        msg,
        reply_markup=InlineKeyboardMarkup(build_menu(WARN_USER_BUTTON, 3)),
        parse_mode=ParseMode.HTML,
    )


@on_update(
    filters=filters.command(["setwarn"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def set_max_warn(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    buttons = [
        InlineKeyboardButton(
            f"{{{button}}}".format_map(Text()), callback_data=f"warn|set|{number}"
        )
        for number, button in SETTING_BUTTON
    ]

    await message(
        update,
        context,
        lang["WARN_SETTING"].format_map(Text()),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 3)),
    )
