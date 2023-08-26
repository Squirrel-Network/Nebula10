#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import copy
import time
from config import Session
from core.utilities.text import Text
from languages import get_group_lang
from core.utilities import constants


async def captcha_cleanup():
    for k, v in copy.deepcopy(Session.captcha).items():
        if (time.monotonic() - v["time"]) >= constants.MAX_TIME_CAPTCHA_CLEANUP:
            _, chat_id = k.split("-", maxsplit=1)
            lang = Session.lang[(await get_group_lang(int(chat_id))).lower()]
            params = {"username": v["username"]}

            await Session.bot.delete_message(chat_id, v["message_id"])

            del Session.captcha[k]

            await Session.bot.send_message(
                chat_id,
                lang["WELCOME_CAPTCHA_CLEANUP"].format_map(Text(params)),
            )
