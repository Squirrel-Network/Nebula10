#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups, GroupSettings
from core.decorators import check_settings, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


async def get_keyboard(update: TelegramUpdate) -> InlineKeyboardMarkup:
    lang_kb = await update.lang_keyboard
    data = await GroupSettings.get(chat_id=update.effective_chat.id)
    is_active = "ACTIVE" if not data.set_welcome else "DEACTIVE"
    buttons = [
        InlineKeyboardButton(
            lang_kb["SETTINGS"][is_active].format_map(Text()),
            callback_data="settings|welcome|state",
        )
    ]

    if data.set_welcome:
        buttons.extend(
            [
                InlineKeyboardButton(
                    lang_kb["SETTINGS"]["WELCOME"][
                        "SETTINGS_WELCOME_SET_MESSAGE"
                    ].format_map(Text()),
                    callback_data="settings|welcome|set_message",
                ),
                InlineKeyboardButton(
                    lang_kb["SETTINGS"]["WELCOME"][
                        "SETTINGS_WELCOME_SEE_MESSAGE"
                    ].format_map(Text()),
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
        lang["SETTINGS"]["WELCOME"]["SETTINGS_WELCOME"].format_map(Text()),
        reply_markup=await get_keyboard(update),
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
async def settings_welcome_set_message_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await update.lang
    lang_kb = await update.lang_keyboard
    key = f"{update.effective_user.id}-{update.effective_chat.id}"

    status = Session.status[key]
    status["status"] = "set_welcome_text"
    status["message_id"] = update.effective_message.message_id
    status["time"] = time.monotonic()
    status["username"] = (
        f"@{update.effective_user.username}" or update.effective_user.first_name
    )

    await update.callback_query.edit_message_text(
        lang["SETTINGS"]["WELCOME"]["SETTINGS_WELCOME_TEXT"].format_map(Text()),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang_kb["CANCEL"].format_map(Text()),
                        callback_data="settings|cancel",
                    )
                ]
            ]
        ),
    )


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
