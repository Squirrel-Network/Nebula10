#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.database.models import Groups, GroupUsers
from core.decorators import check_role, delete_command, on_update
from core.utilities.enums import Role
from core.utilities.menu import build_menu
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


@on_update()
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def init_reply(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    reply = update.effective_message.reply_to_message.from_user
    reason = v[1] if len(v := update.effective_message.text.split()) > 1 else None

    data = await Groups.get(id_group=update.effective_chat.id)
    user = await GroupUsers.get(tg_id=reply.id, tg_group_id=update.effective_chat.id)
    max_warn = data.max_warn
    user_warn = user.warn_count

    params = {
        "name": reply.first_name,
        "count": user_warn + 1,
        "max_warn": max_warn,
        "group_name": update.effective_chat.title,
        "group_id": update.effective_chat.id,
    }
    msg = lang["WARN_USER"].format_map(Text(params))

    if reason:
        params["reason"] = reason
        msg = lang["WARN_USER_REASON"].format_map(Text(params))

    await update.message.reply_to_message.reply_text(
        msg,
        reply_markup=InlineKeyboardMarkup(build_menu(WARN_USER_BUTTON, 3)),
        parse_mode=ParseMode.HTML,
    )
