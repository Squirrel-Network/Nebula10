#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    constants,
)
from telegram.ext import ContextTypes

from core.database.repository.group import GroupRepository
from core.utilities.functions import save_group
from core.utilities.menu import build_menu
from core.utilities.text import Text
from languages import get_lang
from config import Session


async def welcome_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        InlineKeyboardButton(
            text="{GLOBE_WITH_MERIDIANS} Dashboard".format_map(Text()),
            url="https://nebula.squirrel-network.online",
        ),
        InlineKeyboardButton(
            text="{LOUDSPEAKER} Bot_Logs".format_map(Text()),
            url="https://t.me/nebulalogs",
        ),
        InlineKeyboardButton(
            text="{NEWSPAPER} Bot_News".format_map(Text()),
            url="https://t.me/nebulanewsbot",
        ),
        InlineKeyboardButton(
            text="{LARGE_BLUE_DIAMOND} Source Code".format_map(Text()),
            url="https://github.com/Squirrel-Network/nebula10",
        ),
        InlineKeyboardButton(
            text="{BUSTS_IN_SILHOUETTE} Support".format_map(Text()),
            url="https://t.me/nebulabot_support",
        ),
    ]
    params = {
        "version": Session.config.VERSION,
        "version_name": Session.config.VERSION_NAME,
    }

    save_group(update.effective_message.chat_id, update.effective_chat.title)

    await update.message.reply_text(
        get_lang(update)["BOT_WELCOME"].format_map(Text(params)),
        constants.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            # TODO: log
            await welcome_bot(update, context)
