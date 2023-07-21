#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, constants
from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang


@on_update(
    filters=filters.command(["usearch"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    await message(update, context, lang["USEARCH_MSG"])

    await context.bot.send_message(
        update.effective_user.id,
        "Go to Nebula's Public User Search",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Search Users",
                        web_app=WebAppInfo(
                            "https://api.nebula.squirrel-network.online/users#username-anchor"
                        ),
                    )
                ]
            ]
        ),
        parse_mode=constants.ParseMode.HTML,
    )
