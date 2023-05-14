#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.decorators import check_role
from core.utilities.enums import Role
from config import Session
from core.utilities.menu import build_menu
from languages import get_lang
from core.utilities.text import Text


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
async def init(update: Update, _: ContextTypes.DEFAULT_TYPE):
    lang = [(lang, value["LANG_FLAG"]) for lang, value in Session.lang.items()]

    buttons = [
        InlineKeyboardButton(flag.format_map(Text()), callback_data=f"lang|{lang}")
        for lang, flag in lang
    ]

    await update.callback_query.edit_message_text(
        get_lang(update)["SELECT_LANG"],
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
async def change_lang(update: Update, _: ContextTypes.DEFAULT_TYPE):
    # TODO: change lang
    pass
