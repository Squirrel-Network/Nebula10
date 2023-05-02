#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core import decorators
from core.utilities.entities import TelegramObjects
from core.utilities.menu import build_menu
from core.utilities.message import message
from languages import get_lang


@decorators.private.init
@decorators.delete.init
async def init(update, context):
    bot = context.bot
    chat = update.effective_message.chat_id
    get_bot = TelegramObjects(update,context).bot_object()
    user = TelegramObjects(update,context).user_object()
    get_user_lang = user.language_code
    
    if get_user_lang == 'it':
        list_buttons = []
        list_buttons.append(InlineKeyboardButton('Commands', url='https://github.com/Squirrel-Network/nebula8/wiki/Command-List'))
        list_buttons.append(InlineKeyboardButton('Dashboard', url='https://nebula.squirrel-network.online'))
        list_buttons.append(InlineKeyboardButton('Api', url='https://api.nebula.squirrel-network.online'))
        list_buttons.append(InlineKeyboardButton('Knowhere', url='https://squirrel-network.online/knowhere'))
        list_buttons.append(InlineKeyboardButton('News', url='https://t.me/nebulanewsbot'))
        list_buttons.append(InlineKeyboardButton('Logs', url='https://t.me/nebulalogs'))
        list_buttons.append(InlineKeyboardButton('SquirrelNetwork', url='https://t.me/squirrelnetwork'))
        list_buttons.append(InlineKeyboardButton('👥 Add me to a Group', url='https://t.me/thenebulabot?startgroup=start'))
        menu = build_menu(list_buttons, 3)
        text = "🤖 Ciao io mi chiamo {}\n\nSono un bot ricco di funzionalità per la gestione dei gruppi\n"\
               "Possiedo una <b>Blacklist</b> enorme ho un antispam, un antiflood e molto altro ancora!!\n\n"\
               "ℹ Se hai bisogno di aiuto: [/help]\n\n\n🔵 Sapevi che sono OpenSource e cerco sempre aiuto? [/source]".format("@"+get_bot.username)
        await bot.send_message(chat, text, reply_markup=InlineKeyboardMarkup(menu),parse_mode='HTML')
    else:
        await message(update,context,get_lang(update)["START_COMMAND"].format("@"+get_bot.username))