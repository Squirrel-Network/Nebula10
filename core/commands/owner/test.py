#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.decorators import check_role
from core.utilities.enums import Role
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
async def command_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please press the button below to choose a color via the WebApp.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Open WebApp",
                        web_app=WebAppInfo(
                            f"https://webapp.nebula.squirrel-network.online/filters/{update.message.chat_id}"
                        ),
                    )
                ]
            ]
        ),
    )
