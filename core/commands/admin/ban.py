#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from core.database.models import Groups, Users
from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.logs import StringLog, sys_loggers, telegram_loggers
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


async def ban_user_from_id(
    update: TelegramUpdate,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    first_name: str,
    username: str | None,
) -> bool:
    lang = await get_lang(update)

    if user_id == context.bot.id:
        return await message(update, context, lang["BAN_SELF_BAN"])

    chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)

    if chat_member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ):
        return await message(update, context, lang["BAN_ERROR_AC"])

    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    except BadRequest:
        params = {"syntax": user_id}
        return await message(
            update, context, lang["BAN_ERROR_SYNTAX"].format_map(Text(params))
        )

    # Group ban message
    data = await Groups.get(id_group=update.effective_chat.id)
    mention = f'<a href="tg://user?id={user_id}"><>{first_name}</></a>'
    params = {
        "first_name": f"<>{first_name}</>",
        "chat": f"<>{update.effective_chat.title}</>",
        "username": username or mention,
        "mention": mention,
        "userid": user_id,
    }
    await message(update, context, data.ban_message.format_map(Text(params)))

    # Log
    params = {
        "id": user_id,
        "username": username or mention,
        "chat": update.effective_chat.title,
    }

    await telegram_loggers(update, context, StringLog.BAN_LOG.format_map(Text(params)))
    sys_loggers(
        f"Ban eseguito da: {update.effective_message.from_user.id} nella chat {update.effective_chat.id}",
        "info",
    )

    return True


@on_update(
    filters=filters.command(["ban"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.reply
    & filters.group
)
@delete_command
async def init_reply(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.reply_to_message.from_user

    await update.effective_message.reply_to_message.delete()
    await ban_user_from_id(
        update,
        context,
        user.id,
        user.first_name,
        f"@{user.username}" if user.username else None,
    )


@on_update(
    filters=filters.command(["ban"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & ~filters.reply
    & filters.group
)
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    id_or_username = update.effective_message.text.split(maxsplit=1)

    if len(id_or_username) < 2:
        return await message(update, context, lang["BAN_ERROR_NO_ID"])

    id_or_username = id_or_username[1]

    if id_or_username.isnumeric():
        user = await Users.get_or_none(tg_id=int(id_or_username))
    elif id_or_username.startswith("@"):
        user = await Users.get_or_none(tg_username=id_or_username)
    else:
        user = None

    if not user:
        params = {"syntax": id_or_username}
        return await message(
            update, context, lang["BAN_ERROR_SYNTAX"].format_map(Text(params))
        )

    await ban_user_from_id(
        update, context, user.tg_id, user.first_name, user.tg_username
    )


@on_update(
    filters=filters.command(["setban"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & ~filters.reply
    & filters.group
)
@delete_command
async def set_ban_message(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    text = update.effective_message.text.split(maxsplit=1)

    if len(text) == 1:
        return await message(update, context, lang["BAN_EMPTY_ERROR"])

    await Groups.filter(id_group=update.effective_chat.id).update(ban_message=text[1])
    await message(update, context, lang["SET_BAN_MESSAGE"])


@on_update(
    filters=filters.command(["setban"])
    & filters.check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
    & filters.reply
    & filters.reply_text
    & filters.group
)
@delete_command
async def set_ban_message_reply(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
):
    lang = await get_lang(update)
    text = update.effective_message.reply_to_message.text

    await Groups.filter(id_group=update.effective_chat.id).update(ban_message=text)
    await message(update, context, lang["SET_BAN_MESSAGE"])
