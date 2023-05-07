#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import Session
from core.database.repository import GroupRepository
from core.utilities.functions import ban_user, kick_user, mute_user, save_group
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.regex import Regex
from core.utilities.text import Text
from languages import get_lang


NO_USERNAME_ACTION = {
    1: (kick_user, "Kick"),
    2: (None, "Message"),
    3: (mute_user, "Mute"),
    4: (ban_user, "Ban"),
    5: (kick_user, None),
}


def has_arabic_character(data: str) -> bool:
    return bool(re.search(Regex.HAS_ARABIC, data))


def has_cirillic_character(data: str) -> bool:
    return bool(re.search(Regex.HAS_CIRILLIC, data))


def has_chinese_character(string) -> bool:
    return bool(re.search(Regex.HAS_CHINESE, string))


def has_zoophile(data: str):
    return bool(re.search(Regex.HAS_ZOOPHILE, data))


CHECK_NAME = (
    (has_arabic_character, "FILTER_NAME", "set_arabic_filter"),
    (has_cirillic_character, "FILTER_NAME", "set_cirillic_filter"),
    (has_chinese_character, "FILTER_NAME", "set_chinese_filter"),
    (has_zoophile, "BAN_ZOOPHILE", "zoophile_filter"),
)


def check_name(name: str, data: dict) -> str | None:
    for func, text, db in CHECK_NAME:
        if func(name) and data[db]:
            return text


async def welcome_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    save_group(update.effective_message.chat_id, update.effective_chat.title)

    await message(
        update,
        context,
        get_lang(update)["BOT_WELCOME"].format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(build_menu(buttons, 2)),
    )


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with GroupRepository() as db:
        data = db.get_by_id(update.effective_chat.id)

    lang = get_lang(update)
    chat_id = update.effective_chat.id

    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            # TODO: log
            await welcome_bot(update, context)

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
            call = NO_USERNAME_ACTION.get(action, None)
            if exe := call[0]:
                await exe(chat_id, member.id, context)

            if mess := call[1]:
                params = {"user": member.name, "action": mess}

                await message(
                    update,
                    context,
                    lang["KICKED_USER_MESSAGE_NO_USERNAME"].format_map(
                        Text(params)
                    ),
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
            # TODO: save user
            print("TODO")
