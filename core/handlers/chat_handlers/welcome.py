#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes
from core.utilities.entities import TelegramObjects
from core.utilities.functions import save_group
from core.database.repository.group import GroupRepository


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = TelegramObjects().chat_object()

    row = GroupRepository().getById(chat.id)
    if row:
        print("UPDATE")
    else:
        save_group(update.effective_chat.id, update.effective_chat.title)

    await bot.send_message(chat, "Welcome")
