#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

from config import Session
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from core.utilities.token_jwt import encode_jwt
from languages import get_lang


@on_update(
    filters=filters.command(["status"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    await message(update, context, lang["MESSAGE_DB_STATUS"])

    await context.bot.send_message(
        update.effective_user.id,
        lang["STATUS_COMMAND"],
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Open Status",
                        web_app=WebAppInfo(
                            f"{Session.config.WEBAPP_URL}/status?token={encode_jwt()}&chat_id={update.effective_chat.id}"
                        ),
                    )
                ]
            ]
        ),
    )


@on_update(
    filters=filters.command(["chatid"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def chat_id(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    params = {"id": update.effective_chat.id}

    await message(update, context, lang["CHAT_ID_COMMAND"].format_map(Text(params)))
