#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import copy
import time
from config import Session
from core.utilities.text import Text
from languages import get_group_lang
from core.utilities import constants


async def status_cleanup():
    for k, v in copy.deepcopy(Session.status).items():
        if (time.monotonic() - v["time"]) >= constants.MAX_TIME_STATUS_CLEANUP:
            data = k.split("-", maxsplit=1)
            lang = Session.lang[(await get_group_lang(int(data[1]))).lower()]
            params = {"username": v["username"]}

            del Session.status[k]

            await Session.bot.send_message(
                int(data[1]), lang["GROUP_STATUS_CLEANUP"].format_map(Text(params))
            )
