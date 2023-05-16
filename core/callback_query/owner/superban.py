#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import Update, constants
from telegram.ext import ContextTypes

from core.database.repository.superban import SuperbanRepository
from core.decorators import callback_query_regex, check_role
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.text import Text
from languages import get_lang


@check_role(Role.OWNER)
@callback_query_regex("superban|")
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    query = update.callback_query

    if query.data == "superban|remove":
        # TODO: remove superban
        pass
    else:
        motivation = query.data.split("|", 1)[1].replace("_", "")
        user = query.message.reply_to_message.from_user
        operator = query.from_user
        save_date = datetime.datetime.utcnow().isoformat()

        with SuperbanRepository() as db:
            if db.get_whitelist_by_id(user.id):
                params = {"name": user.first_name}

                await message(
                    update,
                    context,
                    lang["SUPERBAN_WHITELIST"].format_map(Text(params)),
                )
            elif db.get_by_id(user.id):
                params = {"id": user.id}

                await message(
                    update,
                    context,
                    lang["SUPERBAN_ALREADY_EXIST"].format_map(Text(params)),
                )
            else:
                db.add(
                    user.id,
                    user.first_name,
                    motivation,
                    save_date,
                    operator.id,
                    f"@{operator.username}",
                    operator.first_name,
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

                # TODO: log
