#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import Session
from core.database.repository.superban import SuperbanRepository
from core.database.repository.user import UserRepository
from core.decorators import check_role
from core.handlers.chat_handlers.logs import debug_channel, sys_loggers
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.text import Text
from languages import get_lang


def check_user(user_id: int, bot_id: int) -> bool:
    with SuperbanRepository() as db:
        blacklist = db.get_by_id(user_id)
        whitelist = db.get_whitelist_by_id(user_id)

    return (
        blacklist
        or whitelist
        or user_id in Session.owner_ids
        or user_id == bot_id
    )


@check_role(Role.OWNER)
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)

    if reply := update.message.reply_to_message:
        buttons = [
            InlineKeyboardButton(
                "{INBOX_TRAY} Spam".format_map(Text()),
                callback_data="superban|spam",
            ),
            InlineKeyboardButton(
                "{WARNING} Scam".format_map(Text()),
                callback_data="superban|scam",
            ),
            InlineKeyboardButton(
                "{ROBOT} Userbot".format_map(Text()),
                callback_data="superban|userbot",
            ),
            InlineKeyboardButton(
                "{NO_ONE_UNDER_EIGHTEEN} Porn".format_map(Text()),
                callback_data="superban|porn",
            ),
            InlineKeyboardButton(
                "{POLICE_OFFICER} Illegal Content".format_map(Text()),
                callback_data="superban|illegal_content",
            ),
            InlineKeyboardButton(
                "{SOS_BUTTON} Harrasment".format_map(Text()),
                callback_data="superban|harrasment",
            ),
            InlineKeyboardButton(
                "{MEMO} Other".format_map(Text()),
                callback_data="superban|other",
            ),
            InlineKeyboardButton(
                "{CROSS_MARK} Remove Superban".format_map(Text()),
                callback_data="superban|remove",
            ),
            InlineKeyboardButton(
                "{WASTEBASKET} Close".format_map(Text()), callback_data="close"
            ),
        ]

        if check_user(reply.from_user.id, context.bot.id):
            return await reply.reply_text(lang["SUPERBAN_ERROR"])

        await reply.reply_text(
            lang["SUPERBAN_REPLY"],
            reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
        )


@check_role(Role.OWNER)
async def remove_superban_via_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    pass


@check_role(Role.OWNER)
async def multi_superban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


@check_role(Role.OWNER)
async def update_superban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
