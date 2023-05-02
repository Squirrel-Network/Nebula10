#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.database.repository.group import GroupRepository
from core.decorators import check_role
from core.utilities.enums import Role
from core.utilities.menu import build_menu
from languages import get_lang


BUTTONS_MENU = (
    ("Welcome 👋🏻", "setWelcome", "set_welcome"),
    ("Silence 🤫", "setSilence", "set_silence"),
    ("Deny All Entry 🚷", "setBlockEntry", "block_new_member"),
    ("AntiFlood 🚫", "setAntiflood", "set_antiflood"),
    ("No User Photo Entry ⛔️", "userPhoto", "set_user_profile_picture"),
    ("No Arabic Entry ⛔️", "arabic", "set_arabic_filter"),
    ("No Russian Entry ⛔️", "cirillic", "set_cirillic_filter"),
    ("No Chinese Entry ⛔️", "chinese", "set_chinese_filter"),
    ("No ZooPhile Entry ⛔️", "zoophile", "zoophile_filter"),
    ("Block Vocal ⛔️", "novocal", "set_no_vocal"),
    ("Block Channel 📢", "channelblock", "sender_chat_block"),
    ("Block Spoiler 🚫", "spoilerblock", "spoiler_block"),
    ("Live with GH 🤖", "setgrouphelp", "set_gh"),
)


def get_keyboard_settings(chat_id: int) -> InlineKeyboardMarkup:
    group = GroupRepository().getById(chat_id)
    buttons = [
        InlineKeyboardButton(
            f"{'✅' if group[db_name] else '❌'} {name}", callback_data=cb
        )
        for name, cb, db_name in BUTTONS_MENU
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
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        update.effective_chat.id,
        get_lang(update)["MAIN_TEXT_SETTINGS"].format(
            update.effective_chat.title, update.effective_chat.id
        ),
        reply_markup=get_keyboard_settings(update.effective_chat.id),
        parse_mode="HTML",
    )
