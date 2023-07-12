#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.start()
