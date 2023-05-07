#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime
import time

from telegram import Update, User, Chat
from telegram.ext import ContextTypes

from config import Session
from core.database.repository.group import GroupRepository
from core.database.repository.user import UserRepository
from core.utilities.constants import PERM_FALSE


def get_owner_list() -> list[int]:
    with UserRepository() as db:
        return [int(x["tg_id"]) for x in db.get_owners()]


async def close_menu(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "close":
        await query.message.delete()


async def kick_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.ban_chat_member(
        chat_id,
        user_id,
        until_date=int(time.time() + 30),
    )


async def mute_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.restrict_chat_member(
        chat_id, user_id, PERM_FALSE
    )


async def ban_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.ban_chat_member(
        chat_id, user_id
    )


def save_group(chat_id: int, chat_title: str):
    with GroupRepository() as db:
        if not db.get_by_id(chat_id):
            dictionary = {
                "id_group": chat_id,
                "group_name": chat_title,
                "welcome_text": Session.config.DEFAULT_WELCOME.format(
                    "{mention}", "{chat}"
                ),
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
                "group_photo": "https://naos.hersel.it/group_photo/default.jpg",
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
                "ban_message": "{mention} has been <b>banned</b> from: {chat}",
                "created_at": datetime.datetime.utcnow().isoformat(),
                "updated_at": datetime.datetime.utcnow().isoformat(),
                "set_gh": 0,
            }

            db.add_with_dict(dictionary)


def save_user(member: User, chat: Chat):
    with UserRepository() as db:
        data = db.get_by_id(member.id)

        current_time = datetime.datetime.utcnow().isoformat()

        if data:
            db.update(member.username, current_time, member.id)
        else:
            db.add(member.id, member.username, current_time, current_time)

        db.add_into_mtm(member.id, chat.id, 0, 0)
