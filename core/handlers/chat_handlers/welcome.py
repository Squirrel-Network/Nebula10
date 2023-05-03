#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.utilities.functions import save_group


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.effective_chat.id

    save_group(update.effective_chat.id, update.effective_chat.title)

    await bot.send_message(chat, "Welcome")
