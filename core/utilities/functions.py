#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

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
        await Groups.create(
            id_group=chat_id,
            group_name=chat_title,
            welcome_text=Session.config.DEFAULT_WELCOME,
            rules_text=Session.config.DEFAULT_RULES,
            languages=Session.config.DEFAULT_LANGUAGE,
            log_channel=Session.config.DEFAULT_LOG_CHANNEL,
        )


async def save_user(member: User, chat: Chat):
    await Users.update_or_create(
        tg_id=member.id, defaults={"tg_username": f"@{member.username}"}
    )

    await GroupUsers.get_or_create(
        tg_id=member.id,
        tg_group_id=chat.id,
        defaults={"warn_count": 0, "user_score": 0},
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


async def mute_user_by_id_time(
    chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE, mute_time=30
):
    await context.bot.restrict_chat_member(
        chat_id, user_id, PERM_FALSE, until_date=int(time.time() + mute_time)
    )
