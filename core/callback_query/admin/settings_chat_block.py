#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import GroupSettings
from core.decorators import check_settings, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


async def get_keyboard_blocks(update: TelegramUpdate) -> InlineKeyboardMarkup:
    lang_kb = await update.lang_keyboard
    data = await (
        await GroupSettings.get(chat_id=update.effective_chat.id)
    ).get_chat_block()
    buttons = [
        InlineKeyboardButton(
            (
                (
                    lang_kb["SETTINGS"]["CHAT_BLOCK"]["ACTIVE_BUTTON"]
                    if v
                    else lang_kb["SETTINGS"]["CHAT_BLOCK"]["DEACTIVE_BUTTON"]
                )
                + lang_kb["SETTINGS"]["CHAT_BLOCK"]["BLOCKS_BUTTONS"][k.upper()]
            ).format_map(Text()),
            callback_data=f"settings|chat_block|blocks|{k}",
        )
        for k, v in data.items()
    ]

    return InlineKeyboardMarkup(
        build_menu(
            buttons,
            2,
            footer_buttons=InlineKeyboardButton(
                lang_kb["BACK"].format_map(Text()), callback_data="settings|chat_block"
            ),
        )
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_chat_block(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await update.lang
    lang_kb = await update.lang_keyboard

    await update.callback_query.edit_message_text(
        lang["SETTINGS"]["CHAT_BLOCK"]["MAIN_TEXT"].format_map(Text()),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang_kb["SETTINGS"]["CHAT_BLOCK"]["BLOCKS"].format_map(Text()),
                        callback_data="settings|chat_block|blocks",
                    )
                ],
                [
                    InlineKeyboardButton(
                        lang_kb["SETTINGS"]["CHAT_BLOCK"]["OBLIGATIONS"].format_map(
                            Text()
                        ),
                        callback_data="settings|chat_block|obligations",
                    )
                ],
                [
                    InlineKeyboardButton(
                        lang_kb["BACK"].format_map(Text()), callback_data="settings"
                    )
                ],
            ]
        ),
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_chat_block_blocks(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await update.lang

    await update.callback_query.edit_message_text(
        lang["SETTINGS"]["CHAT_BLOCK"]["BLOCKS_TEXT"].format_map(Text()),
        reply_markup=await get_keyboard_blocks(update),
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
@check_settings
async def settings_chat_block_blocks_change(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    option = update.callback_query.data.split("|")[-1]

    data = await GroupSettings.get(chat_id=update.effective_chat.id)
    setattr(data, option, not getattr(data, option))
    await data.save()

    await update.callback_query.edit_message_reply_markup(
        await get_keyboard_blocks(update)
    )
