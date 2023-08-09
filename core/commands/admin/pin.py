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
    filters=filters.command(["pin"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
    & filters.reply
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    reply = update.effective_message.reply_to_message

    await reply.pin()

    await message(update, context, lang["PIN_COMMAND"])


@on_update(
    filters=filters.command(["pinned"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def get_pinned(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    last_pin = (await context.bot.get_chat(update.effective_chat.id)).pinned_message

    if not last_pin:
        return await message(update, context, lang["PINNED_COMMAND_ERROR"])

    username_or_id = (
        update.effective_chat.username
        or f"c/{str(update.effective_chat.id).replace('-100', '')}"
    )
    params = {"url": f"t.me/{username_or_id}/{last_pin.message_id}"}

    await message(update, context, lang["PINNED_COMMAND"].format_map(Text(params)))


@on_update(
    filters=filters.command(["unpin"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
    & filters.reply
)
@delete_command
async def unpin(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)

    await update.effective_message.reply_to_message.unpin()

    await message(update, context, lang["UNPIN_COMMAND"])
