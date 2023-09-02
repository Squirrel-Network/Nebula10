#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import constants
from telegram.ext import ContextTypes

from core.database.models import SuperbanTable, WhitelistTable
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.logs import sys_loggers, telegram_loggers
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.check_role(Role.OWNER))
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    query = update.callback_query

    motivation = query.data.split("|", 1)[1].replace("_", "")
    user = query.message.reply_to_message.from_user
    operator = query.from_user
    save_date = datetime.datetime.utcnow().isoformat()

    if await WhitelistTable.exists(tg_id=user.id):
        params = {"name": f"<>{user.first_name}</>"}

        await message(
            update,
            context,
            lang["SUPERBAN_WHITELIST"].format_map(Text(params)),
        )
    elif await SuperbanTable.exists(user_id=user.id):
        params = {"id": user.id}

        await message(
            update,
            context,
            lang["SUPERBAN_ALREADY_EXIST"].format_map(Text(params)),
        )
    else:
        await SuperbanTable.create(
            user_id=user.id,
            user_first_name=user.first_name,
            motivation_text=motivation,
            user_date=save_date,
            id_operator=operator.id,
            username_operator=f"@{operator.username}",
            first_name_operator=operator.first_name,
        )

        params = {"id": user.id, "reason": motivation}
        chat_id = query.message.chat_id

        await context.bot.ban_chat_member(chat_id, user.id)
        await query.edit_message_text(
            lang["SUPERBAN"].format_map(Text(params)),
            parse_mode=constants.ParseMode.HTML,
        )

        await context.bot.delete_message(
            chat_id, query.message.reply_to_message.message_id
        )

        params = {
            "name": f"<>{user.first_name}</>",
            "id": user.id,
            "reason": motivation,
            "date": save_date,
            "operator_name": f"<>{operator.first_name}</>",
            "operator_username": f"@{operator.username}",
            "operator_id": operator.id,
        }
        await telegram_loggers(
            update, context, lang["SUPERBAN_LOG"].format_map(Text(params))
        )

        sys_loggers(
            f"Superban executed by: {operator.username}[<code>{operator.id}</code>] towards the user: [<code>{user.id}</code>].",
            "warning",
        )
