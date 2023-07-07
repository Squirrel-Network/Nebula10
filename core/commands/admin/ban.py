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
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


async def ban_user_from_id(
    update: TelegramUpdate, user_id: int, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)

    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    except BadRequest:
        params = {"syntax": user_id}
        await message(
            update, context, lang["BAN_ERROR_SYNTAX"].format_map(Text(params))
        )

        raise BadRequest("Participant_id_invalid")

    # TODO: log


@on_update
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    reply = update.effective_message.reply_to_message

    if reply:
        user = reply.from_user

        if user.id == context.bot.id:
            return await message(update, context, lang["BAN_SELF_BAN"])

        chat_member = await context.bot.get_chat_member(
            update.effective_chat.id, user.id
        )

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

        await reply.delete()
        await ban_user_from_id(update, user.id, context)
    else:
        id_or_username = update.effective_message.text.split(maxsplit=1)[1]
        params = {"user": id_or_username}

        if id_or_username.isnumeric():
            await ban_user_from_id(update, id_or_username, context)
            return await message(
                update, context, lang["BAN_SUCCESS"].format_map(Text(params))
            )

        data = await Users.get_or_none(tg_username=id_or_username)

        if data:
            await ban_user_from_id(update, data.tg_id, context)
            return await message(
                update, context, lang["BAN_SUCCESS"].format_map(Text(params))
            )

        params = {"syntax": id_or_username}
        await message(
            update, context, lang["BAN_ERROR_SYNTAX"].format_map(Text(params))
        )
