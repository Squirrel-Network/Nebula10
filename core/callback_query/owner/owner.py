#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import constants
from telegram.ext import ContextTypes

from core.database.models import OwnerList
from core.decorators import callback_query_regex, check_role, on_update
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update()
@check_role(Role.OWNER)
@callback_query_regex(r"^owner\|remove$")
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.message.reply_to_message.from_user
    lang = await get_lang(update)

    await OwnerList.filter(tg_id=user.id).delete()

    params = {"name": user.first_name, "id": user.id}
    await update.callback_query.edit_message_text(
        lang["OWNER_REMOVE"].format_map(Text(params)),
        parse_mode=constants.ParseMode.HTML,
    )
