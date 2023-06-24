#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups, NebulaUpdates
from core.decorators import on_update
from core.utilities.functions import check_group_badwords
from core.utilities.logs import telegram_debug_channel
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate


@on_update
async def status(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.chat
    user = update.effective_message.from_user
    msg_update = update.message
    group_members_count = await chat.get_member_count()
    webapp_url = Session.config.WEBAPP_URL

    # This feature changes the chat title on the database when it is changed
    if msg_update.new_chat_title is not None:
        await Groups.filter(id_group=chat.id).update(group_name=chat.title)
        await telegram_debug_channel(
            update,
            context,
            "[DEBUG_LOGGER] La chat <code>[{}]</code> ha cambiato titolo".format(
                chat.id
            ),
        )

    # This function saves the number of users in the group in the database
    if group_members_count > 0:
        await Groups.filter(id_group=chat.id).update(total_users=group_members_count)

    # When a chat room changes group image it is saved to the webserver like this: example.com/group_photo/-100123456789.jpg (url variable)
    if update.effective_message.new_chat_photo:
        if chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            file_id = update.message.new_chat_photo[2].file_id
            newfile = await bot.get_file(file_id)
            folder = "static"

            await newfile.download_to_drive(
                f"core/webapp/{folder}/group_photo/{chat.id}.jpg"
            )
            url = f"{webapp_url}/{folder}/group_photo/{chat.id}.jpg"

            await Groups.filter(id_group=chat.id).update(group_photo=url)
            await telegram_debug_channel(
                update,
                context,
                "[DEBUG_LOGGER] La chat <code>[{}]</code> ha cambiato foto\nIl suo nuovo URL è: {}".format(
                    chat.id, url
                ),
            )

    # This function checks the badwords of the group
    if await check_group_badwords(update, chat.id):
        await bot.delete_message(
            update.effective_message.chat_id, update.message.message_id
        )
        await message(
            update,
            context,
            "<b>#Automatic handler:</b>\n<code>{}</code> You used a forbidden word!".format(
                user.id
            ),
        )

    print("CHAT:\n {}".format(chat))


# this function has the task of saving in the database the updates for the calculation of messages
@on_update
async def check_updates(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.from_user
    chat = update.effective_chat
    date = datetime.datetime.utcnow().isoformat()
    msg_id = update.effective_message.message_id
    upd_id = update.update_id

    if chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        await Groups.filter(id_group=chat.id).update(updated_at=date)
        await NebulaUpdates.get_or_create(
            update_id=upd_id,
            message_id=msg_id,
            tg_group_id=chat.id,
            tg_user_id=user.id,
            date=date,
        )
