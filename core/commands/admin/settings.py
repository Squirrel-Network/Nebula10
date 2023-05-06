#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from core.utilities.message import message
from core.database.repository.group import GroupRepository
from core.decorators import check_role, delete_command
from core.utilities.constants import PERM_FALSE, PERM_TRUE
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from core.utilities.text import Text
from languages import get_lang


BUTTONS_MENU = {
    "settings_set_welcome": ("Welcome 👋🏻", "set_welcome"),
    "settings_set_silence": ("Silence 🤫", "set_silence"),
    "settings_set_block_entry": ("Deny All Entry 🚷", "block_new_member"),
    "settings_set_antiflood": ("AntiFlood 🚫", "set_antiflood"),
    "settings_user_photo": (
        "No User Photo Entry ⛔️",
        "set_user_profile_picture",
    ),
    "settings_arabic": ("No Arabic Entry ⛔️", "set_arabic_filter"),
    "settings_cirillic": ("No Russian Entry ⛔️", "set_cirillic_filter"),
    "settings_chinese": ("No Chinese Entry ⛔️", "set_chinese_filter"),
    "settings_zoophile": ("No ZooPhile Entry ⛔️", "zoophile_filter"),
    "settings_novocal": ("Block Vocal ⛔️", "set_no_vocal"),
    "settings_channel_block": ("Block Channel 📢", "sender_chat_block"),
    "settings_spoiler_block": ("Block Spoiler 🚫", "spoiler_block"),
    "settings_set_group_help": ("Live with GH 🤖", "set_gh"),
}


def get_keyboard_settings(chat_id: int) -> InlineKeyboardMarkup:
    group = GroupRepository().getById(chat_id)
    buttons = [
        InlineKeyboardButton(f"{'✅' if group[v[1]] else '❌'} {v[0]}", callback_data=cb)
        for cb, v in BUTTONS_MENU.items()
    ]

    buttons.extend(
        [
            InlineKeyboardButton("Languages 🌍", callback_data="lang"),
            InlineKeyboardButton(
                "Commands",
                url="https://github.com/Squirrel-Network/nebula8/wiki/Command-List",
            ),
            InlineKeyboardButton(
                "Dashboard", url="https://nebula.squirrel-network.online"
            ),
            InlineKeyboardButton("Close 🗑", callback_data="close"),
        ]
    )

    return InlineKeyboardMarkup(build_menu(buttons, 2))


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    params = {
        "name": update.effective_chat.title,
        "id": update.effective_chat.id,
    }
    await message(
        update,
        context,
        get_lang(update)["MAIN_TEXT_SETTINGS"].format_map(Text(params)),
        reply_markup=get_keyboard_settings(update.effective_chat.id),
    )


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
        GroupRepository().update_group_settings(
            GroupRepository.SET_BLOCK_N_M, [(0, update.effective_chat.id)]
        )


async def settings_set_block_entry(
    update: Update, _: ContextTypes.DEFAULT_TYPE, data: dict
):
    GroupRepository().update_group_settings(
        GroupRepository.SET_WELCOME,
        [(0 if not data["block_new_member"] else 1, update.effective_chat.id)],
    )


SETTINGS_CALLBACK = {
    "settings_set_silence": settings_set_silence,
    "settings_set_welcome": settings_set_welcome,
    "settings_set_block_entry": settings_set_block_entry,
}


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    callback_data = update.callback_query.data
    data = GroupRepository().getById(chat_id)
    value = BUTTONS_MENU[callback_data][1]

    GroupRepository().update_group_settings(value, [(not data[value], chat_id)])

    if callback_data in SETTINGS_CALLBACK:
        await SETTINGS_CALLBACK[callback_data](update, context, data)

    await context.bot.edit_message_reply_markup(
        chat_id,
        update.callback_query.message.id,
        reply_markup=get_keyboard_settings(chat_id),
    )
