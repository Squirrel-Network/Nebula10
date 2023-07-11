#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import callback_query_regex, check_role, on_update
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang

DB_DATA = {"messages": "antiflood_max_messages", "seconds": "antiflood_seconds"}
MAX_MESSAGES = 10


@on_update()
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@callback_query_regex(r"^antiflood\|set\|(messages|seconds)\|minus$")
async def set_antiflood_minus_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    action = update.callback_query.data.split("|")[2]

    data = Groups.filter(id_group=update.effective_chat.id)
    value = (await data.values())[0]

    if value[DB_DATA[action]] == 1:
        return await update.callback_query.answer(lang["ANTIFLOOD_ERROR"])

    await data.update(**{DB_DATA[action]: value[DB_DATA[action]] - 1})

    edit_buttons = [
        [
            InlineKeyboardButton(
                str(value[DB_DATA[action]] - 1), callback_data=col.callback_data
            )
            if col.callback_data == f"antiflood|{action}"
            else col
            for col in row
        ]
        for row in update.callback_query.message.reply_markup.inline_keyboard
    ]

    await update.callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(edit_buttons)
    )


@on_update()
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@callback_query_regex(r"^antiflood\|set\|(messages|seconds)\|plus$")
async def set_antiflood_plus_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    action = update.callback_query.data.split("|")[2]

    data = Groups.filter(id_group=update.effective_chat.id)
    value = (await data.values())[0]

    if value[DB_DATA[action]] == MAX_MESSAGES:
        return await update.callback_query.answer(lang["ANTIFLOOD_ERROR"])

    await data.update(**{DB_DATA[action]: value[DB_DATA[action]] + 1})

    edit_buttons = [
        [
            InlineKeyboardButton(
                str(value[DB_DATA[action]] + 1), callback_data=col.callback_data
            )
            if col.callback_data == f"antiflood|{action}"
            else col
            for col in row
        ]
        for row in update.callback_query.message.reply_markup.inline_keyboard
    ]

    await update.callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(edit_buttons)
    )
