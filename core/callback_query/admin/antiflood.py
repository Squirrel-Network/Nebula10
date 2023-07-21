#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang

BUTTON_NUM = ("antiflood|messages", "antiflood|seconds")
MAX_MESSAGES = 10


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def set_antiflood_minus_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    action = update.callback_query.data.split("|")[2]
    edit_button = []
    value = 1

    for row in update.callback_query.message.reply_markup.inline_keyboard:
        buttons = []
        for col in row:
            if col.callback_data == f"antiflood|{action}":
                value = int(col.text)
                buttons.append(
                    InlineKeyboardButton(
                        str(value - 1), callback_data=col.callback_data
                    )
                )
            else:
                buttons.append(col)
        edit_button.append(buttons)

    if value == 1:
        return await update.callback_query.answer(lang["ANTIFLOOD_ERROR"])

    await update.callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(edit_button)
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def set_antiflood_plus_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    action = update.callback_query.data.split("|")[2]
    edit_button = []
    value = 1

    for row in update.callback_query.message.reply_markup.inline_keyboard:
        buttons = []
        for col in row:
            if col.callback_data == f"antiflood|{action}":
                value = int(col.text)
                buttons.append(
                    InlineKeyboardButton(
                        str(value + 1), callback_data=col.callback_data
                    )
                )
            else:
                buttons.append(col)
        edit_button.append(buttons)

    if value == MAX_MESSAGES:
        return await update.callback_query.answer(lang["ANTIFLOOD_ERROR"])

    await update.callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(edit_button)
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def set_antiflood_success(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    mes, sec = [
        int(col.text)
        for row in update.callback_query.message.reply_markup.inline_keyboard
        for col in row
        if col.callback_data in BUTTON_NUM
    ]

    await Groups.filter(id_group=update.effective_chat.id).update(
        antiflood_max_messages=mes, antiflood_seconds=sec
    )
    await update.callback_query.message.delete()
