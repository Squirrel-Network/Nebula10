#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.utilities import constants
from core.jobs import send_log, status_cleanup, captcha_cleanup


def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(status_cleanup, "interval", seconds=15)
    scheduler.add_job(captcha_cleanup, "interval", seconds=15)
    scheduler.add_job(send_log, "interval", seconds=constants.DAILY)

    scheduler.start()
