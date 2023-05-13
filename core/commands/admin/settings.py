#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update
from telegram.ext import ContextTypes

from core.decorators import check_role, delete_command
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.text import Text
from core.utilities.functions import get_keyboard_settings
from languages import get_lang


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update: Update, context: ContextTypes.DEFAULT_TYPE):
    params = {
        "name": update.effective_chat.title,
        "id": update.effective_chat.id,
    }
    await message(
        update,
        context,
        get_lang(update)["MAIN_TEXT_SETTINGS"].format_map(Text(params)),
        reply_markup=get_keyboard_settings(update.effective_chat.id),
    )
