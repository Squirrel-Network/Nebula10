#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import time

from telegram.ext import ApplicationHandlerStop, ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import on_update
from core.utilities.telegram_update import TelegramUpdate


async def is_flood(chat_id: int, user_id: int) -> bool:
    current_second = int(time.time())
    data = await Groups.get(id_group=chat_id)

    dict_key = f"{user_id}-{chat_id}-{current_second}"

    if not dict_key in Session.antiflood:
        Session.antiflood[dict_key] = 1
    else:
        Session.antiflood[dict_key] += 1

    key_check = [
        f"{user_id}-{chat_id}-{current_second - x}"
        for x in range(data.antiflood_seconds)
    ]
    tot_mess = sum(
        dict(filter(lambda x: x[0] in key_check, Session.antiflood.items())).values()
    )

    return tot_mess > data.antiflood_max_messages


@on_update(True)
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if await is_flood(chat_id, user_id):
        raise ApplicationHandlerStop()
