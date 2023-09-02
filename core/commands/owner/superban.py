#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import SuperbanTable, Users, WhitelistTable
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.logs import sys_loggers, telegram_loggers
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


async def check_user(user_id: int, bot_id: int) -> bool:
    blacklist = await SuperbanTable.exists(user_id=user_id)
    whitelist = await WhitelistTable.exists(tg_id=user_id)

    print(blacklist, whitelist)

    return blacklist or whitelist or user_id in Session.owner_ids or user_id == bot_id


async def new_superban(
    update: TelegramUpdate,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    first_name: str,
    motivation: str,
    save_date: str,
    operator_id: int,
    operator_username: str,
    operator_first_name: str,
    lang: dict[str, str],
):
    await SuperbanTable.create(
        user_id=user_id,
        user_first_name=first_name,
        motivation_text=motivation,
        user_date=save_date,
        id_operator=operator_id,
        username_operator=operator_username,
        first_name_operator=operator_first_name,
    )

    params = {"id": user_id, "reason": motivation}

    await message(update, context, lang["SUPERBAN"].format_map(Text(params)))

    params = {
        "name": f"<>{first_name}</>",
        "id": user_id,
        "reason": motivation,
        "date": save_date,
        "operator_name": f"<>{operator_first_name}</>",
        "operator_username": operator_username,
        "operator_id": operator_id,
    }
    await telegram_loggers(
        update, context, lang["SUPERBAN_LOG"].format_map(Text(params))
    )
    sys_loggers(
        f"Superban executed by: {operator_username}[<code>{operator_id}</code>] towards the user: [<code>{user_id}</code>].",
        "warning",
    )


@on_update(filters=filters.command(["bl"]) & filters.check_role(Role.OWNER))
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    if reply := update.message.reply_to_message:
        buttons = [
            InlineKeyboardButton(
                "{INBOX_TRAY} Spam".format_map(Text()),
                callback_data="superban|spam",
            ),
            InlineKeyboardButton(
                "{WARNING} Scam".format_map(Text()),
                callback_data="superban|scam",
            ),
            InlineKeyboardButton(
                "{ROBOT} Userbot".format_map(Text()),
                callback_data="superban|userbot",
            ),
            InlineKeyboardButton(
                "{NO_ONE_UNDER_EIGHTEEN} Porn".format_map(Text()),
                callback_data="superban|porn",
            ),
            InlineKeyboardButton(
                "{POLICE_OFFICER} Illegal Content".format_map(Text()),
                callback_data="superban|illegal_content",
            ),
            InlineKeyboardButton(
                "{SOS_BUTTON} Harrasment".format_map(Text()),
                callback_data="superban|harrasment",
            ),
            InlineKeyboardButton(
                "{MEMO} Other".format_map(Text()),
                callback_data="superban|other",
            ),
        ]

        if await check_user(reply.from_user.id, context.bot.id):
            return await reply.reply_text(lang["SUPERBAN_ERROR"])

        return await reply.reply_text(
            lang["SUPERBAN_REPLY"],
            reply_markup=InlineKeyboardMarkup(
                build_menu(
                    buttons,
                    2,
                    footer_buttons=InlineKeyboardButton(
                        "{WASTEBASKET} Close".format_map(Text()), callback_data="close"
                    ),
                )
            ),
        )

    text = update.message.text.split()

    if len(text) == 1:
        return await message(update, context, lang["SUPERBAN_ERROR_NO_ID"])

    user_id = text[1]
    motivation = text[2] if len(text) >= 3 else "Other"
    save_date = datetime.datetime.utcnow().isoformat()

    operator_id = update.message.from_user.id
    operator_username = f"@{update.message.from_user.username}"
    operator_first_name = update.message.from_user.first_name

    if user_id.startswith("@"):
        data = await Users.get_or_none(tg_username=user_id)

        if not data:
            return await message(update, context, lang["SUPERBAN_ERROR_USERNAME"])

        await new_superban(
            update,
            context,
            data.tg_id,
            f"NB{data.tg_id}",
            motivation,
            save_date,
            operator_id,
            operator_username,
            operator_first_name,
            lang,
        )

    elif user_id.isdigit():
        if await SuperbanTable.exists(user_id=user_id):
            params = {"id": user_id}

            return await message(
                update,
                context,
                lang["SUPERBAN_ALREADY_EXIST"].format_map(Text(params)),
            )

        await new_superban(
            update,
            context,
            user_id,
            f"NB{user_id}",
            motivation,
            save_date,
            operator_id,
            operator_username,
            operator_first_name,
            lang,
        )

    else:
        await message(update, context, lang["SUPERBAN_ERROR_ID"])


@on_update(filters=filters.command(["ubl"]) & filters.check_role(Role.OWNER))
async def remove_superban_via_id(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    text = update.effective_message.text.split()
    lang = await get_lang(update)

    if len(text) == 1:
        return await message(update, context, lang["SUPERBAN_ERROR_NO_ID"])

    if not text[1].isnumeric():
        return await message(update, context, lang["SUPERBAN_ERROR_ID"])

    user = SuperbanTable.filter(user_id=text[1])

    if not await user.exists():
        return await message(update, context, lang["SUPERBAN_REMOVE_ERROR"])

    await user.delete()

    params = {"id": text[1]}
    await message(update, context, lang["SUPERBAN_REMOVE"].format_map(Text(params)))


@on_update(filters=filters.command(["mbl"]) & filters.check_role(Role.OWNER))
async def multi_superban(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    motivation = "MultiSuperban"
    save_date = datetime.datetime.utcnow().isoformat()
    operator_id = update.message.from_user.id
    operator_username = "@" + update.message.from_user.username
    operator_first_name = update.message.from_user.first_name

    users = [
        (
            x,
            f"NB{x}",
        )
        for x in update.message.text.split(maxsplit=1)[1].split(",")
        if x.isdigit()
    ]

    for user_id, first_name in users:
        await SuperbanTable.create(
            user_id=user_id,
            user_first_name=first_name,
            motivation_text=motivation,
            user_date=save_date,
            id_operator=operator_id,
            username_operator=operator_username,
            first_name_operator=operator_first_name,
        )

    ids_string = [f"{{BLACK_SMALL_SQUARE}} {x[0]}".format_map(Text()) for x in users]

    await message(update, context, lang["SUPERBAN_MULTI"] + "\n".join(ids_string))
