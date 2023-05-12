#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from config import Session
from core.database.repository import GroupRepository
from core.utilities.message import message


LOGGER = {
    "trace": logger.trace,
    "debug": logger.debug,
    "info": logger.info,
    "success": logger.success,
    "warning": logger.warning,
    "error": logger.error,
    "critical": logger.critical,
}


def sys_loggers(message: str, level: str = "trace"):
    LOGGER[level](message)


async def telegram_loggers(
    update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str
):
    chat_id = update.effective_message.chat_id
    log_channel = Session.config.DEFAULT_LOG_CHANNEL

    with GroupRepository() as db:
        data = db.get_by_id(chat_id)

        if data:
            log_channel = data["log_channel"]

    await message(update, context, msg, type="messageid", chat_id=log_channel)
