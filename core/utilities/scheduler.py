#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import copy
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Session
from core.utilities.functions import is_flood

MAX_FLOOD = 10


async def clen_antiflood():
    for cid, v in copy.deepcopy(Session.antiflood).items():
        for uid in v.keys():
            check = list(
                filter(
                    lambda x: time.monotonic() - x < MAX_FLOOD,
                    Session.antiflood[cid][uid],
                )
            )
            if not check:
                del Session.antiflood[cid][uid]


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clen_antiflood, "interval", seconds=10)

    scheduler.start()
