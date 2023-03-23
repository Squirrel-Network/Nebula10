#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from functools import wraps
from core.utilities.functions import get_owner_list

TITLES = ['creator', 'administrator']
OWNER_LIST = get_owner_list()

def admin(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        bot = context.bot
        chat = update.effective_chat.id
        user_id = update.effective_user.id
        get_user = await bot.get_chat_member(chat,user_id)
        stat = get_user.status

        if stat not in TITLES:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped



def owner(func):
    @wraps(func)
    async def wrapped(update, context):
        if update.effective_user is not None:
            user_id = update.effective_user.id
            if user_id not in OWNER_LIST:
                print("Unauthorized access denied for {}.".format(user_id))
                return
        else:
            return False
        return await func(update, context)
    return wrapped
