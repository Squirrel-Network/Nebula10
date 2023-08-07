#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import GroupWelcomeButtons
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.functions import get_welcome_buttons
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def del_welcome_buttons(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    _, _, _, row, column = update.callback_query.data.split("|")

    await update.callback_query.edit_message_text(
        lang["SET_WELCOME_BUTTONS_DEL_CONFIRM"],
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Close {WASTEBASKET}".format_map(Text()), callback_data="close"
                    ),
                    InlineKeyboardButton(
                        "{CHECK_MARK_BUTTON}".format_map(Text()),
                        callback_data=f"welcome|buttons|del|confim|{row}|{column}",
                    ),
                ]
            ]
        ),
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def del_welcome_buttons_confirm(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    _, _, _, _, row, column = update.callback_query.data.split("|")

    data = await GroupWelcomeButtons.get_or_none(
        chat_id=update.effective_chat.id, row=row, column=column
    )

    if not data:
        return await update.callback_query.answer("Error!")

    await data.delete()

    await update.callback_query.edit_message_text(
        lang["SET_WELCOME_BUTTONS"],
        reply_markup=await get_welcome_buttons(update.effective_chat.id),
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def add_welcome_buttons(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    _, _, _, row, column = update.callback_query.data.split("|")
    status = Session.status[f"{update.effective_user.id}-{update.effective_chat.id}"]

    status["status"] = "add_welcome_buttons"
    status["row"] = row
    status["column"] = column
    status["message_id"] = update.effective_message.message_id
    status["time"] = time.monotonic()
    status["username"] = (
        f"@{update.effective_user.username}" or update.effective_user.first_name
    )

    await update.callback_query.edit_message_text(lang["SET_WELCOME_BUTTONS_ADD"])
