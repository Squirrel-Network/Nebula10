#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import OwnerList
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.command(["owner"]) & filters.check_role(Role.OWNER))
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    if not update.message.reply_to_message:
        return await message(update, context, lang["ERROR_MESSAGE_REPLY"])

    user = update.message.reply_to_message.from_user
    user_id = user.id
    user_username = f"@{user.username}"

    if await OwnerList.exists(tg_id=user_id):
        buttons = [
            [
                InlineKeyboardButton(
                    "{CROSS_MARK} Remove".format_map(Text()),
                    callback_data="owner|remove",
                )
            ],
            [
                InlineKeyboardButton(
                    "{WASTEBASKET} Close".format_map(Text()), callback_data="close"
                )
            ],
        ]
        params = {"username": user_username}

        await update.message.reply_to_message.reply_text(
            lang["OWNER_ALREADY_EXIST"].format_map(Text(params)),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await OwnerList.create(tg_id=user_id, tg_username=user_username)
        Session.owner_ids.append(user_id)

        params = {"username": user_username, "id": user_id}

        await message(update, context, lang["OWNER_ADD"].format_map(Text(params)))
