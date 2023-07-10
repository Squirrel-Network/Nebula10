#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram.ext import ContextTypes
from tortoise.exceptions import BaseORMException
from telegram.error import TelegramError

from core.decorators import on_update
from core.utilities.logs import StringLog, telegram_debug_channel
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


@on_update(True)
@logger.catch
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    error = ""

    logger.exception(context.error)

    try:
        raise context.error
    except BaseORMException as e:
        error = f"DB - {type(e).__name__}"

    except TelegramError as e:
        error = e.message

    params = {
        "command_text": update.effective_message.text,
        "error": error,
        "log": context.error,
    }
    await telegram_debug_channel(
        update, context, StringLog.ERROR_LOG.format_map(Text(params))
    )
