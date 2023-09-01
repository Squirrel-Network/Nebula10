#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import itertools

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes

from config import Session
from core.database.models import (
    Groups,
    GroupWelcomeButtons,
    SuperbanTable,
    GroupSettings,
)
from core.decorators import on_update
from core.utilities.captcha import get_catcha
from core.utilities.constants import CUSTOM_BUTTONS_WELCOME
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


async def is_in_blacklist(user_id: int) -> bool:
    return await SuperbanTable.exists(user_id=user_id)


@on_update(True)
async def welcome_bot(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if not update.my_chat_member.new_chat_member.status == ChatMemberStatus.MEMBER:
        return

    buttons = [
        InlineKeyboardButton(
            text="{GLOBE_WITH_MERIDIANS} SquirrelNetwork".format_map(Text()),
            url="https://squirrel-network.online",
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
    welcome_text: str,
):
    buttons = (
        await GroupWelcomeButtons.filter(chat_id=update.effective_chat.id)
        .order_by("row", "column")
        .values()
    )
    buttons = [
        [
            InlineKeyboardButton(
                column["text"],
                **(
                    {"url": column["url"]}
                    if column["url"] not in CUSTOM_BUTTONS_WELCOME
                    else {"callback_data": CUSTOM_BUTTONS_WELCOME[column["url"]]}
                ),
            )
            for column in row
        ]
        for _, row in itertools.groupby(buttons, key=lambda x: x["row"])
    ]
    params = {
        "first_name": f"<>{member.first_name}</>",
        "chat": f"<>{update.effective_chat.title}</>",
        "username": f"@{member.username}" if member.username else member.first_name,
        "mention": f'<a href="tg://user?id={member.id}"><>{member.first_name}</></a>',
        "userid": member.id,
    }

    await message(
        update,
        context,
        welcome_text.format_map(Text(params)),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@on_update(True)
async def new_member(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if not (
        update.chat_member.new_chat_member.status == ChatMemberStatus.MEMBER
        and update.chat_member.old_chat_member.status
        in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED)
    ):
        return

    lang = await get_lang(update)
    chat_id = update.effective_chat.id
    user = update.chat_member.new_chat_member.user

    data = await Groups.get(id_group=chat_id)
    settings = await GroupSettings.get(chat_id=chat_id)

    if await is_in_blacklist(user.id):
        await ban_user(chat_id, user.id, context)

        params = {"id": user.id, "name": f"<>{user.first_name}</>"}

        await message(
            update,
            context,
            lang["USER_ALREADY_BAN"].format_map(Text(params)),
        )

    elif user.id in Session.owner_ids:
        params = {"id": user.id, "name": f"<>{user.name}</>"}
        await message(
            update,
            context,
            lang["OPERATOR_JOIN"].format_map(Text(params)),
        )

    elif settings.block_new_member:
        await kick_user(chat_id, user.id, context)
        await message(update, context, lang["BLOCK_NEW_MEMBER"])

    elif not user.username and (action := data.type_no_username) in NO_USERNAME_ACTION:
        value = NO_USERNAME_ACTION.get(action, None)

        if call := value[0]:
            await call(chat_id, user.id, context)

        if mess := value[1]:
            params = {"user": f"<>{user.name}</>", "action": mess}

            await message(
                update,
                context,
                lang["KICKED_USER_MESSAGE_NO_USERNAME"].format_map(Text(params)),
            )

    elif (
        not (await user.get_profile_photos()).total_count
        and settings.set_user_profile_picture
    ):
        await kick_user(chat_id, user.id, context)

        params = {"id": user.id, "name": f"<>{user.name}</>"}
        await message(
            update,
            context,
            lang["NEW_MEMBER_WITHOUT_PHOTO"].format_map(Text(params)),
        )

    elif text := check_name(user.first_name, await settings.get_settings()):
        await ban_user(chat_id, user.id, context)

        params = {"id": user.id, "name": f"<>{user.name}</>"}
        await message(update, context, lang[text].format_map(Text(params)))

    else:
        await save_user(user, update.effective_chat)

        if settings.set_welcome:
            if settings.set_captcha:
                return await get_catcha(update, context, lang)

            await welcome_user(update, context, user, data.welcome_text)
