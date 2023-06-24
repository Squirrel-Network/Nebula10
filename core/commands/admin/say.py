#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.decorators import check_role, delete_command
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.text import Text
from languages import get_lang


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split(maxsplit=1)

    if not len(command) > 1:
        command.insert(
            1,
            (await get_lang(update))["SAY_MISSING_MESSAGE_WARNING"].format_map(Text()),
        )
    await message(update, context, command[1], allow_sending_without_reply=True)
