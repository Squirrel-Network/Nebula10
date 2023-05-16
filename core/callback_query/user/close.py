#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.decorators import callback_query_regex


@callback_query_regex("close")
async def init(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "close":
        await query.message.delete()
