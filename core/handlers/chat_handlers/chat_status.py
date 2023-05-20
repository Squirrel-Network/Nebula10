#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes
from telegram import Update
from core.database.repository.group import GroupRepository


# from core.handlers.chat_handlers.logs import debug_channel


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg_update = update.effective_message
    group_members_count = await chat.get_member_count()

    # Update Title
    if msg_update.new_chat_title:
        with GroupRepository() as db:
            record_title = GroupRepository.SET_GROUP_NAME
            db.update_group_settings(record_title, chat.title, chat.id)

    # Update Members Count
    if group_members_count > 0:
        print("MEMBRI PRESENTI NEL GRUPPO {}".format(group_members_count))

    print("CHAT:\n {}".format(chat))
