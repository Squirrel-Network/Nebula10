#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def init(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    lang = [(lang, value["LANG_FLAG"]) for lang, value in Session.lang.items()]

    buttons = [
        InlineKeyboardButton(flag.format_map(Text()), callback_data=f"lang|{lang}")
        for lang, flag in lang
    ]

    await update.callback_query.edit_message_text(
        (await get_lang(update))["SELECT_LANG"],
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def change_lang(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    lang = update.callback_query.data.split("|")[1].upper()

    await Groups.filter(id_group=update.effective_chat.id).update(languages=lang)

    await update.callback_query.edit_message_text(
        (await get_lang(update))["LANG_SELECTED"]
    )
