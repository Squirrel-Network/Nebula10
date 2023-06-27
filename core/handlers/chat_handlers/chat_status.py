#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram.constants import ChatType
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups, NebulaUpdates
from core.decorators import on_update
from core.utilities.functions import check_group_badwords
from core.utilities.logs import telegram_debug_channel
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate


# This feature changes the chat title on the database when it is changed
@on_update
async def new_chat_title_handler(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    chat = update.effective_chat

    await Groups.filter(id_group=chat.id).update(group_name=chat.title)
    await telegram_debug_channel(
        update,
        context,
        "[DEBUG_LOGGER] La chat <code>[{}]</code> ha cambiato titolo".format(chat.id),
    )


# When a chat room changes group image it is saved to the webserver like this: example.com/group_photo/-100123456789.jpg (url variable)
@on_update
async def new_chat_photo_handler(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    file_id = update.message.new_chat_photo[2].file_id
    newfile = await context.bot.get_file(file_id)
    chat = update.effective_chat
    folder = "static"

    await newfile.download_to_drive(f"core/webapp/{folder}/group_photo/{chat.id}.jpg")
    url = f"{Session.config.WEBAPP_URL}/{folder}/group_photo/{chat.id}.jpg"

    await Groups.filter(id_group=chat.id).update(group_photo=url)
    await telegram_debug_channel(
        update,
        context,
        f"[DEBUG_LOGGER] La chat <code>[{chat.id}]</code> ha cambiato foto\nIl suo nuovo URL è: {url}",
    )


# this function has the task of saving in the database the updates for the calculation of messages
@on_update
async def check_updates(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.from_user
    chat = update.effective_chat
    date = datetime.datetime.utcnow().isoformat()
    group_members_count = await chat.get_member_count()

    await Groups.filter(id_group=chat.id).update(updated_at=date)
    await NebulaUpdates.get_or_create(
        update_id=update.update_id,
        message_id=update.effective_message.message_id,
        tg_group_id=chat.id,
        tg_user_id=user.id,
        date=date,
    )

    # This function saves the number of users in the group in the database
    if group_members_count > 0:
        await Groups.filter(id_group=chat.id).update(total_users=group_members_count)

    # This function checks the badwords of the group
    if await check_group_badwords(update, chat.id):
        await update.effective_message.delete()
        await message(
            update,
            context,
            f"<b>#Automatic handler:</b>\n<code>{user.id}</code> You used a forbidden word!",
        )
