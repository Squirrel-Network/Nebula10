#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
    constants,
)
from core.decorators import check_role, delete_command
from core.utilities.enums import Role
from core.utilities.message import message
from telegram.ext import ContextTypes


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await message(
        update, context, "Open Search in Private\nNeed Start the bot in private"
    )

    await context.bot.send_message(
        update.effective_user.id,
        "Go to Nebula's Public User Search",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Search Users",
                        web_app=WebAppInfo(
                            "https://api.nebula.squirrel-network.online/users#username-anchor"
                        ),
                    )
                ]
            ]
        ),
        parse_mode=constants.ParseMode.HTML,
    )
