#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(
    filters=filters.command(["say"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split(maxsplit=1)

    if not len(command) > 1:
        command.insert(
            1,
            (await get_lang(update))["SAY_MISSING_MESSAGE_WARNING"].format_map(Text()),
        )
    await message(update, context, command[1], allow_sending_without_reply=True)
