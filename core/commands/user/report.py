#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import Session
from core.decorators import on_update
from core.utilities import filters
from core.utilities.logs import StringLog, telegram_loggers
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(
    filters=filters.command(["report"])
    | filters.command(["admin"], "@") & filters.group
)
async def report(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    link = (update.effective_message.reply_to_message or update.effective_message).link
    params = {
        "id": update.effective_user.id,
        "first_name": f"<>{update.effective_user.first_name}</>",
        "chat_id": update.effective_chat.id,
        "chat_title": f"<>{update.effective_chat.title}</>",
        "link": link,
    }
    text = StringLog.REPORT_MSG.format_map(Text(params))

    await message(update, context, lang["REPORT_ADMIN_MSG"])
    await telegram_loggers(update, context, text)
    await context.bot.send_message(
        Session.config.DEFAULT_STAFF_GROUP,
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Risolto {CHECK_MARK_BUTTON}".format_map(Text()),
                        callback_data="report|resolved",
                    )
                ]
            ]
        ),
        parse_mode=ParseMode.HTML,
    )
