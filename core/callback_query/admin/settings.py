#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import callback_query_regex, check_role
from core.utilities.constants import BUTTONS_MENU, PERM_FALSE, PERM_TRUE
from core.utilities.enums import Role
from core.utilities.functions import get_keyboard_settings


async def settings_set_silence(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict
):
    await context.bot.set_chat_permissions(
        update.effective_chat.id,
        PERM_TRUE if data["set_silence"] else PERM_FALSE,
    )


async def settings_set_welcome(
    update: Update, _: ContextTypes.DEFAULT_TYPE, data: dict
):
    if not data["set_welcome"] and data["block_new_member"]:
        await Groups.filter(id_group=update.effective_chat.id).update(
            block_new_member=0
        )


async def settings_set_block_entry(
    update: Update, _: ContextTypes.DEFAULT_TYPE, data: dict
):
    await Groups.filter(id_group=update.effective_chat.id).update(
        set_welcome=0 if not data["block_new_member"] else 1
    )


SETTINGS_CALLBACK = {
    "settings|set_silence": settings_set_silence,
    "settings|set_welcome": settings_set_welcome,
    "settings|set_block_entry": settings_set_block_entry,
}


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@callback_query_regex("settings|")
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    callback_data = update.callback_query.data

    data = await Groups.get(id_group=chat_id).values()
    value = BUTTONS_MENU[callback_data][1]

    await Groups.filter(id_group=chat_id).update(**{value: not data[value]})

    if callback_data in SETTINGS_CALLBACK:
        await SETTINGS_CALLBACK[callback_data](update, context, data)

    await context.bot.edit_message_reply_markup(
        chat_id,
        update.callback_query.message.id,
        reply_markup=await get_keyboard_settings(chat_id),
    )
