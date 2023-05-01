#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
# Credits https://github.com/PaulSonOfLars/tgbot/

import logging

from config import Session
from core.database.repository.group import GroupRepository
from core.utilities.message import message

SET_CHANNEL_DEBUG = True

def sys_loggers(name="",message="",debugs = False,info = False,warning = False,errors = False, critical = False):
    logger = logging.getLogger(name)
    logger.setLevel((logging.INFO, logging.DEBUG)[Session.config.DEBUG])
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if debugs == True:
        logger.debug(message)
    elif info == True:
        logger.info(message)
    elif warning == True:
        logger.warning(message)
    elif errors == True:
        logger.error(message)
    elif critical == True:
        logger.critical(message)

"""
This function makes a logger on the telegram channel
set if it is not set it is sent to the default channel
"""
def telegram_loggers(update,context,msg = ""):
    chat = update.effective_message.chat_id
    row = GroupRepository().getById([chat])
    id_channel = Session.config.DEFAULT_LOG_CHANNEL
    if row:
        get_log_channel = row['log_channel']
        send = message(update, context, msg, 'HTML', 'messageid', get_log_channel, None)
    else:
        send = message(update, context, msg, 'HTML', 'messageid', id_channel, None)
    return send

def staff_loggers(update,context,msg = ""):
    id_staff_group = Session.config.DEFAULT_STAFF_GROUP
    send = message(update, context, msg, 'HTML', 'messageid', id_staff_group, None)
    return send

def debug_channel(update,context,msg = ""):
    id_debug_channel = -1001540824311
    if SET_CHANNEL_DEBUG == True:
        send = message(update, context, msg, 'HTML', 'messageid', id_debug_channel, None)
    else:
        return
    return send