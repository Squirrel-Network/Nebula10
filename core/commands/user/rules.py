#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.command(["rules"]) & filters.group & ~filters.reply)
@delete_command
async def rules(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    params = {
        "name": f"<>{update.effective_chat.title}</>",
        "id": update.effective_chat.id,
    }

    await message(
        update,
        context,
        lang["RULES_MSG"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang["RULES_BUTTON"].format_map(Text()),
                        callback_data="rules|open",
                    )
                ]
            ]
        ),
    )
