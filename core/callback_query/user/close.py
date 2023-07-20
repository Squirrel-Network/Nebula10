#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities.telegram_update import TelegramUpdate


@on_update()
async def init(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "close":
        await query.message.delete()
