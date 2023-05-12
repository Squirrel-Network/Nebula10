#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
# Credits https://github.com/PaulSonOfLars/tgbot/

from config import Session
from core.utilities.message import message


SET_CHANNEL_DEBUG = True


def staff_loggers(update, context, msg=""):
    id_staff_group = Session.config.DEFAULT_STAFF_GROUP
    send = message(update, context, msg, "HTML", "messageid", id_staff_group, None)
    return send


def debug_channel(update, context, msg=""):
    id_debug_channel = -1001540824311
    if SET_CHANNEL_DEBUG == True:
        send = message(
            update, context, msg, "HTML", "messageid", id_debug_channel, None
        )
    else:
        return
    return send
