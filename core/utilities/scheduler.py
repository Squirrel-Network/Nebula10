#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import copy

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Session
from core.utilities.functions import is_flood


async def clen_antiflood():
    for cid, v in copy.deepcopy(Session.antiflood).items():
        for uid in v.keys():
            if not await is_flood(cid, uid):
                del Session.antiflood[cid][uid]


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clen_antiflood, "interval", seconds=30)

    scheduler.start()
