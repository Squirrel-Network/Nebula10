#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime
import time

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups, GroupsBadwords, GroupUsers, OwnerList, Users
from core.utilities.constants import BUTTONS_MENU, PERM_FALSE
from core.utilities.menu import build_menu


async def get_owner_list() -> list[int]:
    return [x for x, in await OwnerList.all().values_list("tg_id")]


async def kick_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.ban_chat_member(
        chat_id,
        user_id,
        until_date=int(time.time() + 30),
    )


async def mute_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.restrict_chat_member(chat_id, user_id, PERM_FALSE)


async def ban_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.ban_chat_member(chat_id, user_id)


async def save_group(chat_id: int, chat_title: str):
    if not (await Groups.exists(id_group=chat_id)):
        dictionary = {
            "id_group": chat_id,
            "group_name": chat_title,
            "welcome_text": Session.config.DEFAULT_WELCOME,
            "welcome_buttons": '{"buttons": [{"id": 0,"title": "Bot Logs","url": "https://t.me/nebulalogs"}]}',
            "rules_text": Session.config.DEFAULT_RULES,
            "community": 0,
            "languages": Session.config.DEFAULT_LANGUAGE,
            "set_welcome": 1,
            "max_warn": 3,
            "set_silence": 0,
            "exe_filter": 0,
            "block_new_member": 0,
            "set_arabic_filter": 0,
            "set_cirillic_filter": 0,
            "set_chinese_filter": 0,
            "set_user_profile_picture": 0,
            "gif_filter": 0,
            "set_cas_ban": 1,
            "type_no_username": 1,
            "log_channel": Session.config.DEFAULT_LOG_CHANNEL,
            "group_photo": "https://naos.hersel.it/group_photo/default.jpg",
            "total_users": 0,
            "zip_filter": 0,
            "targz_filter": 0,
            "jpg_filter": 0,
            "docx_filter": 0,
            "apk_filter": 0,
            "zoophile_filter": 1,
            "sender_chat_block": 1,
            "spoiler_block": 0,
            "set_no_vocal": 0,
            "set_antiflood": 1,
            "ban_message": "{mention} has been <b>banned</b> from: {chat}",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "updated_at": datetime.datetime.utcnow().isoformat(),
        }

        await Groups.create(**dictionary)


async def save_user(member: User, chat: Chat):
    current_time = datetime.datetime.utcnow().isoformat()

    await Users.update_or_create(
        tg_id=member.id,
        tg_username=f"@{member.username}",
        created_at=current_time,
        updated_at=current_time,
    )

    await GroupUsers.get_or_create(
        tg_id=member.id, tg_group_id=chat.id, warn_count=0, user_score=0
    )


async def get_keyboard_settings(chat_id: int) -> InlineKeyboardMarkup:
    group = await Groups.get(id_group=chat_id).values()

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


# Check Badwords in chat
async def check_group_badwords(update: Update, chat_id: int):
    bad_word = update.effective_message.text or update.effective_message.caption
    if bad_word is not None:
        return await GroupsBadwords.exists(tg_group_id=chat_id, word=bad_word)
