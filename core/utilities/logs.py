#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate

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
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE, msg: str
):
    chat_id = update.effective_message.chat_id
    log_channel = Session.config.DEFAULT_LOG_CHANNEL

    data = await Groups.get_or_none(id_group=chat_id)

    if data:
        log_channel = data.log_channel

    await message(update, context, msg, type="messageid", chat_id=log_channel)


async def telegram_debug_channel(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE, msg: str
):
    id_debug_channel = Session.config.DEFAULT_DEBUG_CHANNEL

    await message(update, context, msg, "HTML", "messageid", id_debug_channel, None)


class StringLog:
    BAN_LOG = (
        "<b>{WARNING} #Log User Banned!</b>\n{BUST_IN_SILHOUETTE} User_Id: <code>{ID}</code>\n"
        '{BUST_IN_SILHOUETTE} Username: <a href="tg://user?id={ID}">{USERNAME}</a>\n'
        "{BUSTS_IN_SILHOUETTE} Group: {CHAT}\n"
    )
