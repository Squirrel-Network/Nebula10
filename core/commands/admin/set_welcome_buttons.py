#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from config import Session
from core.database.models import GroupWelcomeButtons
from core.decorators import delete_command, on_update
from core.utilities import constants, filters
from core.utilities.enums import Role
from core.utilities.functions import get_welcome_buttons
from core.utilities.message import message
from core.utilities.regex import Regex
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang


@on_update(
    filters=filters.command(["welcomebuttons"])
    & filters.group
    & ~filters.reply
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
)
@delete_command
async def set_welcome_buttons(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)

    await message(
        update,
        context,
        lang["SET_WELCOME_BUTTONS"],
        reply_markup=await get_welcome_buttons(update.effective_chat.id),
    )


@on_update(
    filters=filters.group
    & ~filters.reply
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.check_status("add_welcome_buttons")
    & filters.text
)
async def add_button_status(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    text = [x.strip() for x in update.effective_message.text.split("-")]
    key = f"{update.effective_user.id}-{update.effective_chat.id}"
    status = Session.status[key]

    if (
        len(text) < 2
        or not Regex.is_url(text[1])
        and text[1] not in constants.CUSTOM_BUTTONS_WELCOME
    ):
        del Session.status[key]

        return await message(update, context, lang["SET_WELCOME_BUTTONS_ADD_ERROR"])

    await GroupWelcomeButtons.create(
        chat_id=update.effective_chat.id,
        row=status["row"],
        column=status["column"],
        text=text[0],
        url=text[1],
    )
    await context.bot.delete_message(update.effective_chat.id, status["message_id"])

    del Session.status[key]

    await message(
        update,
        context,
        lang["SET_WELCOME_BUTTONS"],
        reply_markup=await get_welcome_buttons(update.effective_chat.id),
    )
