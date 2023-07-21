#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities import filters
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.command(["help"]))
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    buttons = [
        InlineKeyboardButton(
            text="📖 Command List",
            url="https://github.com/Squirrel-Network/nebula8/wiki/Command-List",
        ),
        InlineKeyboardButton(
            text="🆓 Source", url="https://github.com/Squirrel-Network/nebula10"
        ),
        InlineKeyboardButton("🔔 Logs Channel", url="https://t.me/nebulalogs"),
        InlineKeyboardButton("📣 News Channel", url="https://t.me/nebulanewsbot"),
        InlineKeyboardButton(
            text="🚷 BlackList", url="https://squirrel-network.online/knowhere"
        ),
        InlineKeyboardButton(
            text="📑 API Docs",
            url="https://api.nebula.squirrel-network.online/apidocs",
        ),
        InlineKeyboardButton("🌐 Network SN", url="https://t.me/squirrelnetwork"),
        InlineKeyboardButton(
            "🛠 Dashboard", url="https://nebula.squirrel-network.online"
        ),
        InlineKeyboardButton("Close 🗑", callback_data="close"),
    ]
    params = {"name": f"@{bot.username}"}

    await message(
        update,
        context,
        (await get_lang(update))["HELP_COMMAND"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )
