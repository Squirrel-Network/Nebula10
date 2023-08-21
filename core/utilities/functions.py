#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import html
import itertools
import time

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.ext import ContextTypes
from tortoise.exceptions import ValidationError

from config import Session
from core.database.models import (
    Groups,
    GroupsBadwords,
    GroupSettings,
    GroupsFilters,
    GroupUsers,
    GroupWelcomeButtons,
    OwnerList,
    Users,
)
from core.utilities.constants import BUTTONS_SETTINGS, PERM_ALL_TRUE, PERM_FALSE
from core.utilities.menu import build_menu
from core.utilities.text import Text


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


async def unmute_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.restrict_chat_member(chat_id, user_id, PERM_ALL_TRUE)


async def ban_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.ban_chat_member(chat_id, user_id)


async def save_group(chat_id: int, chat_title: str):
    chat_title = html.escape(chat_title)

    group, created = await Groups.get_or_create(
        id_group=chat_id,
        defaults={
            "group_name": chat_title,
            "welcome_text": Session.config.DEFAULT_WELCOME,
            "rules_text": Session.config.DEFAULT_RULES,
            "languages": Session.config.DEFAULT_LANGUAGE,
            "log_channel": Session.config.DEFAULT_LOG_CHANNEL,
        },
    )

    if not created:
        await group.update_from_dict({"group_name": chat_title}).save()

    await GroupsFilters.update_or_create(chat_id=chat_id)
    await GroupSettings.update_or_create(chat_id=chat_id)


async def save_user(member: User, chat: Chat):
    await Users.update_or_create(
        tg_id=member.id,
        defaults={
            "first_name": html.escape(member.first_name),
            "tg_username": (f"@{member.username}" if member.username else None),
        },
    )

    await GroupUsers.get_or_create(
        tg_id=member.id,
        tg_group_id=chat.id,
        defaults={"warn_count": 0, "user_score": 0},
    )


async def get_keyboard_settings(chat_id: int, page: int) -> InlineKeyboardMarkup:
    limit = Session.config.MAX_ELEMENTS_PAGE * 2
    offset = (page - 1) * limit

    data = await (await GroupSettings.get(chat_id=chat_id)).get_settings()
    group = dict(list(data.items())[offset : (offset + limit)])

    buttons = [
        InlineKeyboardButton(
            f"{'{CHECK_MARK_BUTTON}' if v else '{CROSS_MARK}'} {BUTTONS_SETTINGS[k]}".format_map(
                Text()
            ),
            callback_data=f"settings|select|{k}|{int(v)}|{page}",
        )
        for k, v in group.items()
    ]

    page_buttons = []
    buttons = build_menu(buttons, 2)

    if page > 1:
        page_buttons.append(
            InlineKeyboardButton(
                "{LEFT_ARROW}".format_map(Text()),
                callback_data=f"settings|page|{page - 1}",
            )
        )
    if len(data) > (offset + limit):
        page_buttons.append(
            InlineKeyboardButton(
                "{RIGHT_ARROW}".format_map(Text()),
                callback_data=f"settings|page|{page + 1}",
            )
        )

    buttons.extend(
        [
            page_buttons,
            [
                InlineKeyboardButton(
                    "Languages {GLOBE_SHOWING_EUROPE_AFRICA}".format_map(Text()),
                    callback_data="lang",
                ),
                InlineKeyboardButton("Close 🗑", callback_data="close"),
            ],
        ]
    )

    return InlineKeyboardMarkup(buttons)


async def get_welcome_buttons(chat_id: int):
    result = []
    buttons = (
        await GroupWelcomeButtons.filter(chat_id=chat_id)
        .order_by("row", "column")
        .values()
    )

    for i, row in itertools.groupby(buttons, key=lambda x: x["row"]):
        tmp = []
        for column in row:
            tmp.append(
                InlineKeyboardButton(
                    column["text"],
                    callback_data=f"welcome|buttons|del|{column['row']}|{column['column']}",
                )
            )

        if len(tmp) < Session.config.MAX_KEYBOARD_COLUMN:
            tmp.append(
                InlineKeyboardButton(
                    "{PLUS}".format_map(Text()),
                    callback_data=f"welcome|buttons|add|{column['row']}|{column['column'] + 1}",
                )
            )

        result.append(tmp)

    if len(result) < Session.config.MAX_KEYBOARD_ROW:
        result.append(
            [
                InlineKeyboardButton(
                    "{PLUS}".format_map(Text()),
                    callback_data="welcome|buttons|add|0|0"
                    if not buttons
                    else f"welcome|buttons|add|{i + 1}|0",
                )
            ]
        )

    result.append(
        [
            InlineKeyboardButton(
                "Close {WASTEBASKET}".format_map(Text()), callback_data="close"
            )
        ]
    )

    return InlineKeyboardMarkup(result)


# Check Badwords in chat
async def check_group_badwords(update: Update) -> bool:
    bad_word = update.effective_message.text or update.effective_message.caption

    if bad_word is not None:
        try:
            return await GroupsBadwords.exists(
                tg_group_id=update.effective_chat.id, word=bad_word
            )
        except ValidationError:
            return False


async def mute_user_by_id_time(
    chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE, mute_time=30
):
    await context.bot.restrict_chat_member(
        chat_id, user_id, PERM_FALSE, until_date=int(time.time() + mute_time)
    )
