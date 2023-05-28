#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram import Update
from telegram.ext import ContextTypes

from config import Session
from core.utilities.enums import Role


def check_role(*roles: Role):
    def decorator(func: typing.Callable):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = await update.effective_chat.get_member(update.effective_user.id)

            if user.status in roles:
                return await func(update, context)

            elif Role.OWNER in roles and update.effective_user.id in Session.owner_ids:
                return await func(update, context)

            return

        return wrapper

    return decorator
