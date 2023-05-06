#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from config import Session
from core.database.repository.user import UserRepository
from core.database.repository.group import GroupRepository


def get_owner_list() -> list[int]:
    with UserRepository() as db:
        return [int(x["tg_id"]) for x in db.getOwners()]


async def close_menu(update, context):
    query = update.callback_query

    if query.data == 'close':
        await query.message.delete()


def save_group(chat_id: int, chat_title: str):
    if not GroupRepository().getById(chat_id):
        dictionary = {
            "id_group": chat_id,
            "group_name": chat_title,
            "welcome_text": Session.config.DEFAULT_WELCOME.format("{mention}","{chat}"),
            "welcome_buttons": '{"buttons": [{"id": 0,"title": "Bot Logs","url": "https://t.me/nebulalogs"}]}',
            "rules_text": Session.config.DEFAULT_RULES,
            "community": 0,
            "languages": Session.config.DEFAULT_LANGUAGE,
            "set_welcome": 1,
            "max_warn": 3,
            "set_silence": 0,
            "exe_filter": 0,
            "block_new_member": 0,
            "set_arabic_filter": 0,
            "set_cirillic_filter": 0,
            "set_chinese_filter": 0,
            "set_user_profile_picture": 0,
            "gif_filter": 0,
            "set_cas_ban": 1,
            "type_no_username": 1,
            "log_channel": Session.config.DEFAULT_LOG_CHANNEL,
            "group_photo": 'https://naos.hersel.it/group_photo/default.jpg',
            "total_users": 0,
            "zip_filter": 0,
            "targz_filter": 0,
            "jpg_filter": 0,
            "docx_filter": 0,
            "apk_filter": 0,
            "zoophile_filter": 1,
            "sender_chat_block": 1,
            "spoiler_block": 0,
            "set_no_vocal": 0,
            "set_antiflood": 1,
            "ban_message": '{mention} has been <b>banned</b> from: {chat}',
            "created_at": datetime.datetime.utcnow().isoformat(),
            "updated_at": datetime.datetime.utcnow().isoformat(),
            "set_gh": 0
        }
        
        GroupRepository().add_with_dict(dictionary)
