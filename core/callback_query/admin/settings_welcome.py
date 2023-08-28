#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import Groups, GroupSettings
from core.decorators import check_settings, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


async def get_keyboard(update: TelegramUpdate) -> InlineKeyboardMarkup:
    lang_kb = await update.lang_keyboard
    data = await GroupSettings.get(chat_id=update.effective_chat.id)
    is_active = (
        "SETTINGS_WELCOME_STATE_ACTIVE"
        if not data.set_welcome
        else "SETTINGS_WELCOME_STATE_DEACTIVE"
    )
    buttons = [
        InlineKeyboardButton(
            lang_kb[is_active].format_map(Text()),
            callback_data="settings|welcome|state",
        )
    ]

    if data.set_welcome:
        buttons.extend(
            [
                InlineKeyboardButton(
                    lang_kb["SETTINGS_WELCOME_SET_MESSAGE"].format_map(Text()),
                    callback_data="settings|welcome|set_message",
                ),
                InlineKeyboardButton(
                    lang_kb["SETTINGS_WELCOME_SEE_MESSAGE"].format_map(Text()),
                    callback_data="settings|welcome|see_message",
                ),
            ]
        )

    buttons.append(
        InlineKeyboardButton(
            lang_kb["BACK"].format_map(Text()), callback_data="settings"
        )
    )

    return InlineKeyboardMarkup([[x] for x in buttons])


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_welcome(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await update.lang

    await update.callback_query.edit_message_text(
        lang["SETTINGS_WELCOME"], reply_markup=await get_keyboard(update)
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_welcome_state_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    data = await GroupSettings.get(chat_id=update.effective_chat.id)

    data.set_welcome = not data.set_welcome
    await data.save()

    await update.callback_query.edit_message_reply_markup(await get_keyboard(update))


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_welcome_see_message_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang_kb = await update.lang_keyboard
    data = await Groups.get(id_group=update.effective_chat.id)

    await update.callback_query.edit_message_text(
        data.welcome_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang_kb["BACK"].format_map(Text()),
                        callback_data="settings|welcome",
                    )
                ]
            ]
        ),
    )