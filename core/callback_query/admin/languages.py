#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import callback_query_regex, check_role
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.text import Text
from languages import get_lang


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@callback_query_regex("^lang$")
async def init(update: Update, _: ContextTypes.DEFAULT_TYPE):
    lang = [(lang, value["LANG_FLAG"]) for lang, value in Session.lang.items()]

    buttons = [
        InlineKeyboardButton(flag.format_map(Text()), callback_data=f"lang|{lang}")
        for lang, flag in lang
    ]

    await update.callback_query.edit_message_text(
        (await get_lang(update))["SELECT_LANG"],
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@callback_query_regex("^lang\|([a-zA-Z]+)$")
async def change_lang(update: Update, _: ContextTypes.DEFAULT_TYPE):
    lang = update.callback_query.data.split("|")[1].upper()

    await Groups.filter(id_group=update.effective_chat.id).update(languages=lang)

    await update.callback_query.edit_message_text(
        (await get_lang(update))["LANG_SELECTED"]
    )
