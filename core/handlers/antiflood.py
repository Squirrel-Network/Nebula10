#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import time

from telegram.ext import ApplicationHandlerStop, ContextTypes

from config import Session
from core.decorators import on_update
from core.utilities.functions import is_flood
from core.utilities.telegram_update import TelegramUpdate


@on_update(True)
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    Session.antiflood[chat_id][user_id].append(time.monotonic())

    if await is_flood(chat_id, user_id):
        raise ApplicationHandlerStop()
