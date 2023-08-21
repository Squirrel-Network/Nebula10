#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import html
import json
import traceback

from loguru import logger
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes
from tortoise.exceptions import BaseORMException

from config import Session
from core.decorators import on_update
from core.utilities.logs import StringLog, telegram_debug_channel
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text


@on_update(True)
@logger.catch
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    error = ""

    logger.exception(context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )

    try:
        raise context.error
    except BaseORMException as e:
        error = f"DB - {type(e).__name__}"

    except TelegramError as e:
        error = e.message
    except BaseException as e:
        error = type(e).__name__

    # Send message to debug channel
    params = {
        "command_text": update.effective_message.text
        if update.effective_message
        else "None",
        "error": error,
        "log": context.error,
    }
    await telegram_debug_channel(
        update, context, StringLog.ERROR_LOG.format_map(Text(params))
    )

    # Send message to Dev
    params = {
        "update": html.escape(
            json.dumps(update.to_dict(), indent=2, ensure_ascii=False)
        ),
        "chat_data": html.escape(str(context.chat_data)),
        "user_data": html.escape(str(context.user_data)),
        "error": html.escape("".join(tb_list)),
    }

    for user_id in Session.config.DEVELOPERS_CHAT_ID:
        await context.bot.send_message(
            user_id, StringLog.ERROR_DM_DEV_LOG.format_map(Text(params)), ParseMode.HTML
        )
