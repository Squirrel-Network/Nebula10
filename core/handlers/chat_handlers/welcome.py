#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import json

from telegram import (
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberRestricted,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
)
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups, SuperbanTable
from core.decorators import on_update
from core.utilities.functions import (
    ban_user,
    kick_user,
    mute_user,
    save_group,
    save_user,
)
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.regex import Regex
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang

NO_USERNAME_ACTION = {
    1: (kick_user, "Kick"),
    2: (None, "Message"),
    3: (mute_user, "Mute"),
    4: (ban_user, "Ban"),
    5: (kick_user, None),
}


CHECK_NAME = (
    (Regex.has_arabic_character, "FILTER_NAME", "set_arabic_filter"),
    (Regex.has_cirillic_character, "FILTER_NAME", "set_cirillic_filter"),
    (Regex.has_chinese_character, "FILTER_NAME", "set_chinese_filter"),
    (Regex.has_zoophile, "BAN_ZOOPHILE", "zoophile_filter"),
)


def check_name(name: str, data: dict) -> str | None:
    for func, text, db in CHECK_NAME:
        if func(name) and data[db]:
            return text


def is_in_blacklist(user_id: int) -> bool:
    return SuperbanTable.exists(user_id=user_id)


@on_update
async def welcome_bot(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.new_chat_member.status in (
        ChatMemberBanned,
        ChatMemberLeft,
        ChatMemberRestricted,
    ):
        return

    buttons = [
        InlineKeyboardButton(
            text="{GLOBE_WITH_MERIDIANS} Dashboard".format_map(Text()),
            url="https://nebula.squirrel-network.online",
        ),
        InlineKeyboardButton(
            text="{LOUDSPEAKER} Bot_Logs".format_map(Text()),
            url="https://t.me/nebulalogs",
        ),
        InlineKeyboardButton(
            text="{NEWSPAPER} Bot_News".format_map(Text()),
            url="https://t.me/nebulanewsbot",
        ),
        InlineKeyboardButton(
            text="{LARGE_BLUE_DIAMOND} Source Code".format_map(Text()),
            url="https://github.com/Squirrel-Network/nebula10",
        ),
        InlineKeyboardButton(
            text="{BUSTS_IN_SILHOUETTE} Support".format_map(Text()),
            url="https://t.me/nebulabot_support",
        ),
    ]
    params = {
        "version": Session.config.VERSION,
        "version_name": Session.config.VERSION_NAME,
    }

    await save_group(update.effective_chat.id, update.effective_chat.title)

    await message(
        update,
        context,
        (await get_lang(update))["BOT_WELCOME"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


async def welcome_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    member: User,
    data: dict,
):
    buttons = [
        InlineKeyboardButton(x["title"], url=x["url"])
        for x in json.loads(data["welcome_buttons"])["buttons"]
    ]
    params = {
        "first_name": member.first_name,
        "chat": update.effective_chat.title,
        "username": f"@{member.username}" if member.username else member.first_name,
        "mention": f'<a href="tg://user?id={member.id}">{member.first_name}</a>',
        "userid": member.id,
    }

    await message(
        update,
        context,
        data["welcome_text"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


@on_update
async def new_member(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    data = await Groups.get(id_group=update.effective_chat.id).values()

    lang = await get_lang(update)
    chat_id = update.effective_chat.id

    for member in update.message.new_chat_members:
        if is_in_blacklist(member.id):
            await ban_user(chat_id, member.id, context)

            params = {"id": member.id, "name": member.first_name}

            await message(
                update,
                context,
                lang["USER_ALREADY_BAN"].format_map(Text(params)),
            )

        elif member.id in Session.owner_ids:
            params = {"id": member.id, "name": member.name}
            await message(
                update,
                context,
                lang["OPERATOR_JOIN"].format_map(Text(params)),
            )

        elif data["block_new_member"]:
            await kick_user(chat_id, member.id, context)
            await message(update, context, lang["BLOCK_NEW_MEMBER"])

        elif (
            not member.username
            and (action := data["type_no_username"]) in NO_USERNAME_ACTION
        ):
            value = NO_USERNAME_ACTION.get(action, None)

            if call := value[0]:
                await call(chat_id, member.id, context)

            if mess := value[1]:
                params = {"user": member.name, "action": mess}

                await message(
                    update,
                    context,
                    lang["KICKED_USER_MESSAGE_NO_USERNAME"].format_map(Text(params)),
                )

        elif (
            not (await member.get_profile_photos()).total_count
            and data["set_user_profile_picture"]
        ):
            await kick_user(chat_id, member.id, context)

            params = {"id": member.id, "name": member.name}
            await message(
                update,
                context,
                lang["NEW_MEMBER_WITHOUT_PHOTO"].format_map(Text(params)),
            )

        elif text := check_name(member.name, data):
            await ban_user(chat_id, member.id, context)

            params = {"id": member.id, "name": member.name}
            await message(update, context, lang[text].format_map(Text(params)))

        else:
            await save_user(member, update.effective_chat)

            if not data:
                params = {
                    "username": update.effective_chat.username,
                    "name": update.effective_chat.title,
                }
                await message(
                    update,
                    context,
                    Session.config.DEFAULT_WELCOME.format_map(Text(params)),
                )

            else:
                await welcome_user(update, context, member, data)
