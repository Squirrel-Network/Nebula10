#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import callback_query_regex, on_update
from core.utilities.telegram_update import TelegramUpdate


@on_update()
@callback_query_regex(r"close")
async def init(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "close":
        await query.message.delete()
