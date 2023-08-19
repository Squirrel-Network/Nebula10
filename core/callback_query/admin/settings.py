#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.database.models import GroupSettings
from core.decorators import on_update
from core.utilities import filters
from core.utilities.constants import PERM_FALSE, PERM_TRUE
from core.utilities.enums import Role
from core.utilities.functions import get_keyboard_settings
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


async def settings_set_silence(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE, value: bool
):
    await context.bot.set_chat_permissions(
        update.effective_chat.id,
        PERM_TRUE if value else PERM_FALSE,
    )


async def settings_set_welcome(
    update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE, value: bool
):
    if not value:
        await GroupSettings.filter(chat_id=update.effective_chat.id).update(
            block_new_member=0
        )


async def settings_set_block_entry(
    update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE, value: bool
):
    await GroupSettings.filter(chat_id=update.effective_chat.id).update(
        set_welcome=0 if not value else 1
    )


SETTINGS_CALLBACK = {
    "set_silence": settings_set_silence,
    "set_welcome": settings_set_welcome,
    "block_new_member": settings_set_block_entry,
}


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    callback_data = update.callback_query.data.split("|")
    db_key = callback_data[-3]
    value = bool(int(callback_data[-2]))
    page = int(callback_data[-1])

    await GroupSettings.filter(chat_id=chat_id).update(**{db_key: not value})

    if db_key in SETTINGS_CALLBACK:
        await SETTINGS_CALLBACK[db_key](update, context, value)

    await update.callback_query.edit_message_reply_markup(
        await get_keyboard_settings(chat_id, page)
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def settings_page(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    page = int(update.callback_query.data.split("|")[-1])
    params = {"name": update.effective_chat.title, "id": update.effective_chat.id}

    await update.callback_query.edit_message_text(
        lang["MAIN_TEXT_SETTINGS"].format_map(Text(params)),
        reply_markup=await get_keyboard_settings(update.effective_chat.id, page),
        parse_mode=ParseMode.HTML,
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def settings_modern(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Work in progress!")
