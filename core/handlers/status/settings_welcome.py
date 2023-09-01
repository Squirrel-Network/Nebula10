#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from config import Session
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.functions import is_valid_html


@on_update(
    True,
    filters.group
    & ~filters.reply
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.check_status("set_welcome_text")
    & filters.text,
)
async def set_welcome_text_status(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    key = f"{update.effective_user.id}-{update.effective_chat.id}"

    print(is_valid_html(update.effective_message.text))
