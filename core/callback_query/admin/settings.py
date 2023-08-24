#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities import filters
from core.utilities.constants import SETTING_BUTTONS
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def settings(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await update.lang
    lang_kb = await update.lang_keyboard
    params = {"name": update.effective_chat.title, "id": update.effective_chat.id}

    await update.callback_query.edit_message_text(
        lang["MAIN_TEXT_SETTINGS"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang_kb[name].format_map(Text()), callback_data=cb
                    )
                    for name, cb in x
                ]
                for x in SETTING_BUTTONS
            ]
            + [
                [
                    InlineKeyboardButton(
                        lang_kb["LANG"].format_map(Text()), callback_data="lang"
                    ),
                    InlineKeyboardButton(
                        lang_kb["CLOSE"].format_map(Text()), callback_data="close"
                    ),
                ]
            ]
        ),
        parse_mode=ParseMode.HTML,
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def settings_modern(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Work in progress!")
