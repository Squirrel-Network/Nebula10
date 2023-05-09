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

        return await reply.reply_text(
            lang["SUPERBAN_REPLY"],
            reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
        )

    text = update.message.text.split()

    if len(text) == 1:
        return await message(update, context, lang["SUPERBAN_ERROR_NO_ID"])

    user_id = text[1]
    motivation = text[2] if len(text) >= 3 else "Other"
    save_date = datetime.datetime.utcnow().isoformat()

    operator_id = update.message.from_user.id
    operator_username = f"@{update.message.from_user.username}"
    operator_first_name = update.message.from_user.first_name

    if user_id.startswith("@"):
        with UserRepository() as db:
            data = db.get_by_username(user_id)

        if not data:
            return await message(
                update, context, lang["SUPERBAN_ERROR_USERNAME"]
            )

        with SuperbanRepository() as db:
            db.add(
                data["tg_id"],
                f"NB{data['tg_id']}",
                motivation,
                save_date,
                operator_id,
                operator_username,
                operator_first_name,
            )

        params = {"id": data["tg_id"], "reason": motivation}

        await message(
            update, context, lang["SUPERBAN_USERNAME"].format_map(Text(params))
        )

        # TODO: log
    elif user_id.isdigit():
        with SuperbanRepository() as db:
            data = db.get_by_id(int(user_id))

            if data:
                params = {"id": user_id}

                return await message(
                    update,
                    context,
                    lang["SUPERBAN_ALREADY_EXIST"].format_map(Text(params)),
                )

            db.add(
                user_id,
                f"NB{user_id}",
                motivation,
                save_date,
                operator_id,
                operator_username,
                operator_first_name,
            )

        params = {"id": user_id, "reason": motivation}

        await message(
            update, context, lang["SUPERBAN_ID"].format_map(Text(params))
        )

        # TODO: log
    else:
        await message(update, context, lang["SUPERBAN_ERROR_ID"])


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
