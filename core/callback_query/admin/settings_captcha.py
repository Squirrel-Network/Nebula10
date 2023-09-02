#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import GroupSettings
from core.decorators import check_settings, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


async def get_keyboard(update: TelegramUpdate) -> InlineKeyboardMarkup:
    lang_kb = await update.lang_keyboard
    data = await GroupSettings.get(chat_id=update.effective_chat.id)

    is_active = "ACTIVE" if not data.set_captcha else "DEACTIVE"

    buttons = [
        InlineKeyboardButton(
            lang_kb["SETTINGS"][is_active].format_map(Text()),
            callback_data="settings|captcha|state",
        )
    ]

    buttons.append(
        InlineKeyboardButton(
            lang_kb["BACK"].format_map(Text()), callback_data="settings"
        )
    )

    return InlineKeyboardMarkup([[x] for x in buttons])


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_captcha(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await update.lang

    await update.callback_query.edit_message_text(
        lang["SETTINGS"]["CAPTCHA"]["MAIN_TEXT"].format_map(Text()),
        reply_markup=await get_keyboard(update),
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_captcha_state_cb(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    data = await GroupSettings.get(chat_id=update.effective_chat.id)

    data.set_captcha = not data.set_captcha
    await data.save()

    await update.callback_query.edit_message_reply_markup(await get_keyboard(update))
