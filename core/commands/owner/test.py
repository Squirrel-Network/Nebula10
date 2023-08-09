#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities import filters
from core.utilities.captcha import get_catcha
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate


@on_update(
    filters=filters.command(["test"]) & filters.check_role(Role.OWNER) & filters.private
)
async def command_test(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    image, keyboard = get_catcha(update.effective_user.id)

    await message(
        update, context, "test", type="photo", img=image, reply_markup=keyboard
    )
