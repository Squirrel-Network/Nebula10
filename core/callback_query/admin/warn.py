#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.database.models import Groups, GroupUsers
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def warn_down(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = update.effective_message.reply_to_message.from_user

    max_warn = (await Groups.get(id_group=chat_id)).max_warn
    data = GroupUsers.filter(tg_id=user.id, tg_group_id=chat_id)
    user_warn = (await data.first()).warn_count - 1

    if user_warn < 0:
        return await query.edit_message_text(lang["WARN_DOWN_ERR"], ParseMode.HTML)

    await data.update(warn_count=user_warn)

    params = {"id": user.id, "warn_count": user_warn, "max_warn": max_warn}
    await query.edit_message_text(
        lang["WARN_DOWN"].format_map(Text(params)), ParseMode.HTML
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def warn_up(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = update.effective_message.reply_to_message.from_user

    max_warn = (await Groups.get(id_group=chat_id)).max_warn
    data = GroupUsers.filter(tg_id=user.id, tg_group_id=chat_id)
    user_warn = (await data.first()).warn_count + 1

    if user_warn > max_warn:
        await context.bot.ban_chat_member(chat_id, user.id)
        return await query.edit_message_text(lang["WARN_UP_ERR"], ParseMode.HTML)

    await data.update(warn_count=user_warn)

    params = {"id": user.id, "warn_count": user_warn, "max_warn": max_warn}
    await query.edit_message_text(
        lang["WARN_UP"].format_map(Text(params)), ParseMode.HTML
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def warn_del(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = update.effective_message.reply_to_message.from_user

    await GroupUsers.filter(tg_id=user.id, tg_group_id=chat_id).update(warn_count=0)

    params = {"id": user.id}
    await query.edit_message_text(
        lang["WARN_DEL"].format_map(Text(params)), ParseMode.HTML
    )


@on_update(filters=filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR))
async def set_max_warn_cb(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    value = update.callback_query.data.split("|")[2]

    await Groups.filter(id_group=update.effective_chat.id).update(max_warn=value)

    params = {"warn_count": value}
    await update.callback_query.edit_message_text(
        lang["WARN_SETTING_SUCCESS"].format_map(Text(params)), ParseMode.HTML
    )
