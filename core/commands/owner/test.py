#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate


@on_update(
    filters=filters.command(["test"]) & filters.check_role(Role.OWNER) & filters.private
)
async def command_test(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please press the button below to choose a color via the WebApp.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Open WebApp",
                        web_app=WebAppInfo(
                            f"https://webapp.nebula.squirrel-network.online/filters/{update.message.chat_id}"
                        ),
                    )
                ]
            ]
        ),
    )
