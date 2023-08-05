#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities.telegram_update import TelegramUpdate


@on_update()
async def init(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    text = update.callback_query.message.text
    text += f"\n<b>Fixed by: @{update.effective_user.username}</b>"

    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)
