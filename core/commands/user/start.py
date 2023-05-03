#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.decorators import delete_command, private_chat
from core.utilities.menu import build_menu
from languages import get_lang


START_BUTTONS = (
    ("Commands", "https://github.com/Squirrel-Network/nebula8/wiki/Command-List"),
    ("Dashboard", "https://nebula.squirrel-network.online"),
    ("Api", "https://api.nebula.squirrel-network.online"),
    ("Knowhere", "https://squirrel-network.online/knowhere"),
    ("News", "https://t.me/nebulanewsbot"),
    ("Logs", "https://t.me/nebulalogs"),
    ("SquirrelNetwork", "https://t.me/squirrelnetwork"),
    ("👥 Add me to a Group", "https://t.me/thenebulabot?startgroup=start"),
)


@private_chat
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        InlineKeyboardButton(name, url=url)
        for name, url in START_BUTTONS
    ]
    
    await context.bot.send_message(
        update.effective_message.chat_id, 
        get_lang(update)["START_COMMAND"].format("@"+context.bot.username),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 3)),
        parse_mode='HTML'
    )