#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.database.models import GroupPinnedMessage
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang
from core.utilities.text import Text


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
    await GroupPinnedMessage.create(
        chat_id=update.effective_chat.id, message_id=reply.message_id
    )

    await message(update, context, lang["PIN_COMMAND"])


@on_update(
    filters=filters.command(["pinned"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.group
)
@delete_command
async def get_pinned(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    pin_num = update.effective_message.text.split()
    pin_num = pin_num[1] if len(pin_num) > 1 else "0"
    pin_num = int(pin_num) if pin_num.isdigit() else 0

    data = (
        await GroupPinnedMessage.filter(chat_id=update.effective_chat.id)
        .order_by("-created_at")
        .values()
    )

    if pin_num >= len(data):
        return await message(update, context, lang["PINNED_COMMAND_ERROR"])

    username_or_id = (
        update.effective_chat.username
        or f"c/{str(update.effective_chat.id).replace('-100', '')}"
    )
    params = {"url": f"t.me/{username_or_id}/{data[pin_num]['message_id']}"}

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

    data = await GroupPinnedMessage.get_or_none(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.reply_to_message.id,
    )

    if not data:
        return await message(update, context, lang["UNPIN_COMMAND_ERROR"])

    await update.effective_message.reply_to_message.unpin()
    await data.delete()

    await message(update, context, lang["UNPIN_COMMAND"])
