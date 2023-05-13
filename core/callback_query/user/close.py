#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes


async def init(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "close":
        await query.message.delete()
