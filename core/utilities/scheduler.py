#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import copy
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Session
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


def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(status_cleanup, "interval", seconds=15)

    scheduler.start()
