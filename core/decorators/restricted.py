#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram import Update
from telegram.ext import ContextTypes

from core.utilities.enums import Role
from config import Session


def check_role(*roles: Role):
    def decorator(func: typing.Callable):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            get_user = await context.bot.get_chat_member(
                update.effective_chat.id, 
                update.effective_user.id
            )

            if get_user.status in roles:
                return await func(update, context)
            
            elif (
                Role.OWNER in roles and 
                update.effective_user.id in Session.owner_ids
            ):
                return await func(update, context)
            
            return
        return wrapper
    return decorator
