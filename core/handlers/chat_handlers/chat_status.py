#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import Update
from telegram.ext import ContextTypes

from core.database.repository.group import GroupRepository
from core.utilities import constants as CONST
from core.decorators import on_update
from core.utilities.telegram_update import TelegramUpdate

# from core.handlers.chat_handlers.logs import debug_channel


@on_update
async def status(update: TelegramUpdate, _: ContextTypes.DEFAULT_TYPE):
    chat = update.chat
    msg_update = update.update.effective_message
    group_members_count = await chat.get_member_count()

    """
    This feature changes the chat title
    on the database when it is changed
    """
    if msg_update.new_chat_title:
        with GroupRepository() as db:
            record_title = GroupRepository.SET_GROUP_NAME
            db.update_group_settings(record_title, chat.title, chat.id)

    """
    This function saves the number
    of users in the group in the database
    """
    if group_members_count > 0:
        with GroupRepository() as db:
            record_members = GroupRepository.SET_GROUP_MEMBERS_COUNT
            db.update_group_settings(record_members, group_members_count, chat.id)

    print("CHAT:\n {}".format(chat))


"""
this function has the task of saving
in the database the updates
for the calculation of messages
"""


async def check_updates(update: Update):
    user = update.effective_message.from_user
    chat = update.effective_chat
    date = datetime.datetime.utcnow().isoformat()
    msg_id = update.effective_message.message_id
    upd_id = update.update_id
    if chat.type == CONST.SUPERGROUP or chat.type == CONST.GROUP:
        record_updated_at = GroupRepository.UPDATED_AT
        with GroupRepository() as db:
            data = [(upd_id, msg_id, chat.id, user.id, date)]
            db.update_group_settings(record_updated_at, date, chat.id)
            db.insert_updates(data)
