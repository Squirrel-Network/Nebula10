#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
    constants,
)
from telegram.ext import ContextTypes

from config import Session
from core.decorators import check_role, delete_command
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.text import Text
from core.utilities.token_jwt import TokenJwt, encode_jwt
from languages import get_lang


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    params = {"name": update.message.chat.title, "chat_id": update.message.chat_id}
    token = TokenJwt(update.effective_user.id, update.effective_chat.id)

    await message(update, context, lang["MESSAGE_DM_FILTERS"])

    await context.bot.send_message(
        update.effective_user.id,
        lang["FILTERS_COMMAND"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Open filters settings",
                        web_app=WebAppInfo(
                            f"{Session.config.WEBAPP_URL}/filters/{encode_jwt(token)}"
                        ),
                    )
                ]
            ]
        ),
        parse_mode=constants.ParseMode.HTML,
    )
