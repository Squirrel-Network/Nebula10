#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from loguru import logger
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes

from core.decorators import check_role, delete_command, on_update
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


@on_update()
@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
@logger.catch
async def init_reply(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    user = update.effective_message.reply_to_message.from_user

    user_status = await context.bot.get_chat_member(update.effective_chat.id, user.id)
    params = {
        "user": f'<a href="tg://user?id={user.id}">{user.first_name}</a>',
        "id": user.id,
    }

    if user_status.status != ChatMemberStatus.BANNED:
        return await message(
            update, context, lang["UNBAN_ERROR"].format_map(Text(params))
        )

    await context.bot.unban_chat_member(update.effective_chat.id, user.id)
    await message(update, context, lang["UNBAN_SUCCESS"].format_map(Text(params)))
