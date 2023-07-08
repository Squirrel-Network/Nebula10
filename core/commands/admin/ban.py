#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from core.database.models import Groups, Users
from core.decorators import check_role, delete_command, on_update
from core.utilities.enums import Role
from core.utilities.logs import StringLog, sys_loggers, telegram_loggers
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


async def ban_user_from_id(
    update: TelegramUpdate, user_id: int, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    lang = await get_lang(update)

    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    except BadRequest:
        params = {"syntax": user_id}
        await message(
            update, context, lang["BAN_ERROR_SYNTAX"].format_map(Text(params))
        )

        return False

    reply = update.effective_message.reply_to_message or update.effective_message
    params = {
        "id": reply.from_user.id,
        "username": reply.from_user.username or reply.from_user.first_name,
        "chat": update.effective_chat.title,
    }

    await telegram_loggers(update, context, StringLog.BAN_LOG.format_map(Text(params)))
    sys_loggers(
        f"Ban eseguito da: {update.effective_message.from_user.id} nella chat {update.effective_chat.id}",
        "info",
    )

    return True


@on_update
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def init_reply(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    user = update.effective_message.reply_to_message.from_user

    if user.id == context.bot.id:
        return await message(update, context, lang["BAN_SELF_BAN"])

    chat_member = await context.bot.get_chat_member(update.effective_chat.id, user.id)

    if chat_member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ):
        return await message(update, context, lang["BAN_ERROR_AC"])

    data = await Groups.get(id_group=update.effective_chat.id)

    params = {
        "first_name": user.first_name,
        "chat": update.effective_chat.title,
        "username": f"@{user.username}" if user.username else user.first_name,
        "mention": f'<a href="tg://user?id={user.id}">{user.first_name}</a>',
        "userid": user.id,
    }

    await message(update, context, data.ban_message.format_map(Text(params)))

    await update.effective_message.reply_to_message.delete()
    await ban_user_from_id(update, user.id, context)


@on_update
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    id_or_username = update.effective_message.text.split(maxsplit=1)[1]
    params = {"user": id_or_username}

    if not id_or_username.isnumeric():
        data = await Users.get_or_none(tg_username=id_or_username)

        if not data:
            params = {"syntax": id_or_username}
            return await message(
                update, context, lang["BAN_ERROR_SYNTAX"].format_map(Text(params))
            )

        id_or_username = data.tg_id

    result = await ban_user_from_id(update, id_or_username, context)
    if result:
        await message(update, context, lang["BAN_SUCCESS"].format_map(Text(params)))


@on_update
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def set_ban_message(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    text = update.effective_message.text.split(maxsplit=1)

    if len(text) == 1:
        return await message(update, context, lang["BAN_EMPTY_ERROR"])

    await Groups.filter(id_group=update.effective_chat.id).update(ban_message=text[1])
    await message(update, context, lang["SET_BAN_MESSAGE"])


@on_update
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def set_ban_message_reply(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    text = update.effective_message.reply_to_message.text

    await Groups.filter(id_group=update.effective_chat.id).update(ban_message=text)
    await message(update, context, lang["SET_BAN_MESSAGE"])
