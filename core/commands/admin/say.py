#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update, constants
from telegram.ext import ContextTypes

from core.decorators import check_role, delete_command
from core.utilities.enums import Role
from languages import get_lang


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split(maxsplit=1)

    if not len(command) > 1:
        command.insert(1, get_lang(update)["SAY_MISSING_MESSAGE_WARNING"])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=command[1],
        parse_mode=constants.ParseMode.HTML,
        allow_sending_without_reply=True,
    )
