#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import itertools
import copy
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Session
from core.database.models import GroupPinnedMessage
from core.utilities.text import Text
from languages import get_group_lang

MAX_TIME_STATUS_CLEANUP = 3 * 60


async def status_cleanup():
    for k, v in copy.deepcopy(Session.status).items():
        if (time.monotonic() - v["time"]) >= MAX_TIME_STATUS_CLEANUP:
            data = k.split("-", maxsplit=1)
            lang = Session.lang[(await get_group_lang(int(data[1]))).lower()]
            params = {"username": v["username"]}

            del Session.status[k]

            await Session.bot.send_message(
                int(data[1]), lang["GROUP_STATUS_CLEANUP"].format_map(Text(params))
            )


async def pinned_message():
    data = await GroupPinnedMessage.all().order_by("created_at").values()

    for chat_id, value in itertools.groupby(data, lambda x: x["chat_id"]):
        await Session.bot.unpin_all_chat_messages(chat_id)

        for x in value:
            await Session.bot.pin_chat_message(
                chat_id, x["message_id"], disable_notification=True
            )


def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(status_cleanup, "interval", seconds=15)
    scheduler.add_job(pinned_message, "interval", hours=1)

    scheduler.start()
