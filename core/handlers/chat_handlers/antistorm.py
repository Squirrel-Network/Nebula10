#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import time

from telegram.constants import ChatMemberStatus
from telegram.ext import ApplicationHandlerStop, ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate

MAX_ANTISTORM_SIZE = 85


async def is_storm(chat_id: int) -> bool:
    current_second = int(time.time())
    data = await Groups.get(id_group=chat_id)

    dict_key = f"{chat_id}-{current_second}"

    if not dict_key in Session.antistorm:
        Session.antistorm[dict_key] = 1
    else:
        Session.antistorm[dict_key] += 1

    key_check = [
        f"{chat_id}-{current_second - x}" for x in range(data.antistorm_seconds)
    ]
    tot_income = sum(
        dict(filter(lambda x: x[0] in key_check, Session.antistorm.items())).values()
    )

    return tot_income > data.antistorm_max_users


@on_update(True, ~filters.check_role(Role.OWNER, Role.ADMINISTRATOR, Role.CREATOR))
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    if not (
        update.chat_member.new_chat_member.status == ChatMemberStatus.MEMBER
        and update.chat_member.old_chat_member.status
        in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED)
    ):
        return

    chat_id = update.effective_chat.id

    if len(Session.antistorm) > (
        Session.antistorm.max_len * (MAX_ANTISTORM_SIZE / 100)
    ):
        Session.antistorm.max_len *= 2

    if await is_storm(chat_id):
        print("storm")
        # TODO: action to user

        raise ApplicationHandlerStop()
