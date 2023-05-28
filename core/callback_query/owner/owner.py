#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram import constants
from telegram.ext import ContextTypes

from core.database.repository import UserRepository
from core.decorators import callback_query_regex, on_update
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update
@callback_query_regex("owner|remove")
@logger.catch
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.message.reply_to_message.from_user
    lang = get_lang(update)

    with UserRepository() as db:
        db.remove_owner(user.id)

    params = {"name": user.first_name, "id": user.id}
    await update.callback_query.edit_message_text(
        lang["OWNER_REMOVE"].format_map(Text(params)),
        parse_mode=constants.ParseMode.HTML,
    )
