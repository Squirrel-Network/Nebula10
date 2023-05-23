#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from telegram import Update
from telegram.ext import ContextTypes

from core.database.repository.group import GroupRepository
from core.decorators import on_update
from core.utilities import constants as CONST
from core.utilities.telegram_update import TelegramUpdate

# from core.handlers.chat_handlers.logs import debug_channel


@on_update
async def status(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.chat
    msg_update = update.message
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

    """
     When a chat room changes group image it is saved to the webserver
     like this: example.com/group_photo/-100123456789.jpg (url variable)
    """
    if update.effective_message.new_chat_photo:
        if chat.type == CONST.SUPERGROUP or chat.type == CONST.GROUP:
            file_id = update.message.new_chat_photo[2].file_id
            newfile = await bot.get_file(file_id)
            #TODO AttributeError: 'File' object has no attribute 'download'
            #newfile.download('/var/www/naos.hersel.it/group_photo/{}.jpg'.format(chat.id))
            url = "https://naos.hersel.it/group_photo/{}.jpg".format(chat.id)
            print(url)
            print(newfile)

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
