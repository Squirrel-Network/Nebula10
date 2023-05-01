#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core.utilities.menu import build_menu
from languages import get_lang


async def init(update,context):
    bot = context.bot
    chat = update.effective_message.chat_id
    msg = get_lang(update)["HELP_COMMAND"].format("@"+bot.username)
    buttons = []
    buttons.append(InlineKeyboardButton("Commands List", url='https://github.com/Squirrel-Network/nebula8/wiki/Command-List'))
    buttons.append(InlineKeyboardButton("Source", url='https://github.com/Squirrel-Network/nebula10'))
    buttons.append(InlineKeyboardButton("Logs Channel", url='https://t.me/nebulalogs'))
    buttons.append(InlineKeyboardButton("News Channel", url='https://t.me/nebulanewsbot'))
    buttons.append(InlineKeyboardButton("BlackList Search", url='https://squirrel-network.online/knowhere'))
    buttons.append(InlineKeyboardButton("Official API Docs", url='https://api.nebula.squirrel-network.online/apidocs'))
    buttons.append(InlineKeyboardButton("Network SN", url='https://t.me/squirrelnetwork'))
    menu = build_menu(buttons,3)
    await bot.send_message(chat,msg,reply_markup=InlineKeyboardMarkup(menu))