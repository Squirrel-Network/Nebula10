#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import on_update
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update()
async def init(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    msg_rules = (await Groups.get(id_group=update.effective_chat.id)).rules_text
    params = {"rules": msg_rules}

    await update.callback_query.edit_message_text(
        lang["RULES"].format_map(Text(params))
    )
