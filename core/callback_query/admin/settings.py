#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.database.repository import GroupRepository
from core.decorators import check_role
from core.utilities.constants import PERM_FALSE, PERM_TRUE
from core.utilities.enums import Role
from core.utilities.functions import get_keyboard_settings
from core.utilities.constants import BUTTONS_MENU


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
        with GroupRepository() as db:
            db.update_group_settings(
                GroupRepository.SET_BLOCK_N_M, 0, update.effective_chat.id
            )


async def settings_set_block_entry(
    update: Update, _: ContextTypes.DEFAULT_TYPE, data: dict
):
    with GroupRepository() as db:
        db.update_group_settings(
            GroupRepository.SET_WELCOME,
            0 if not data["block_new_member"] else 1,
            update.effective_chat.id,
        )


SETTINGS_CALLBACK = {
    "settings|set_silence": settings_set_silence,
    "settings|set_welcome": settings_set_welcome,
    "settings|set_block_entry": settings_set_block_entry,
}


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    callback_data = update.callback_query.data

    with GroupRepository() as db:
        data = db.get_by_id(chat_id)
        value = BUTTONS_MENU[callback_data][1]

        db.update_group_settings(value, not data[value], chat_id)

    if callback_data in SETTINGS_CALLBACK:
        await SETTINGS_CALLBACK[callback_data](update, context, data)

    await context.bot.edit_message_reply_markup(
        chat_id,
        update.callback_query.message.id,
        reply_markup=get_keyboard_settings(chat_id),
    )
