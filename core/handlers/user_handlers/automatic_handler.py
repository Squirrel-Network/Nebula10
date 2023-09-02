#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes
from telegram.constants import MessageEntityType

from core.database.models import Groups, GroupUsers, SuperbanTable, GroupSettings
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.functions import (
    ban_user,
    check_group_badwords,
    kick_user,
    mute_user,
    save_user,
)
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang

NO_USERNAME_ACTION = {
    1: (kick_user, "KICK"),
    2: (None, "WARNING"),
    3: (mute_user, "MUTE"),
    4: (ban_user, "BAN"),
    5: (kick_user, None),
}


@on_update(
    True,
    ~filters.check_role(Role.ADMINISTRATOR, Role.CREATOR, Role.OWNER)
    & ~filters.service
    & filters.group
    & filters.user
    & ~filters.users({777000}),
)
async def status(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    user = update.effective_user
    chat = update.effective_chat

    superban = await SuperbanTable.get_or_none(user_id=user.id)
    group = await Groups.get(id_group=chat.id)
    settings = await GroupSettings.get(chat_id=chat.id)
    user_data = await GroupUsers.get_or_none(tg_id=user.id, tg_group_id=chat.id)

    params = {"id": user.id, "name": f"<>{user.first_name}</>"}

    if superban:
        params["reason"] = superban.motivation_text

        await message(
            update, context, lang["AUTOMATIC_HANDLER_SUPERBAN"].format_map(Text(params))
        )
        await ban_user(chat.id, user.id, context)
        await update.effective_message.delete()
        return

    elif not user.username and (action := group.type_no_username) in NO_USERNAME_ACTION:
        value = NO_USERNAME_ACTION.get(action, None)

        if call := value[0]:
            await call(chat.id, user.id, context)

        if mess := value[1]:
            await message(
                update,
                context,
                lang[f"AUTOMATIC_HANDLER_USERNAME_{mess}"].format_map(Text(params)),
            )
        return

    elif (
        not (await user.get_profile_photos()).total_count
        and settings.set_user_profile_picture
    ):
        await kick_user(chat.id, user.id, context)
        await message(
            update, context, lang["AUTOMATIC_HANDLER_NO_PHOTO"].format_map(Text(params))
        )
        return

    elif user_data and group.max_warn <= user_data.warn_count:
        await ban_user(chat.id, user.id, context)
        await message(
            update, context, lang["AUTOMATIC_HANDLER_MAX_WARN"].format_map(Text(params))
        )
        return

    # This function checks the badwords of the group
    elif await check_group_badwords(update):
        await update.effective_message.delete()
        await message(
            update,
            context,
            lang["AUTOMATIC_HANDLER_BAD_WORD"].format_map(Text(params)),
        )
        return

    # This function is used to filter messages with spoiler type
    # and delete them if the group owner puts the block at 1
    spoiler = [
        x
        for x in update.effective_message.entities
        if x.type == MessageEntityType.SPOILER
    ]
    if spoiler and settings.spoiler_block:
        await update.effective_message.delete()
        await message(update, context, lang["AUTOMATIC_HANDLER_SPOILER"])

    # This function checks if messages
    # are arriving from a channel and deletes them
    elif (v := update.effective_message.sender_chat) and settings.sender_chat_block:
        if v.id == update.effective_chat.linked_chat_id:
            return

        params["id"] = chat.id
        params["name"] = v.title
        params["channel_id"] = v.id

        await update.effective_message.delete()
        await message(
            update, context, lang["AUTOMATIC_HANDLER_CHANNEL"].format_map(Text(params))
        )
        return

    # Voice audio blocking
    elif update.effective_message.voice and settings.set_no_vocal:
        await update.effective_message.delete()
        await message(update, context, lang["AUTOMATIC_HANDLER_VOICE"])

    await save_user(user, chat)
