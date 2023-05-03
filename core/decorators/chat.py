#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import functools
import typing

from telegram import Update
from telegram.ext import ContextTypes


PRIVATE_CHAT = "private"
PUBLIC_CHAT = ("supergroup", "group")


def private_chat(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type == PRIVATE_CHAT:
            return await func(update, context)
        
        return
    return wrapper


def public_chat(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type in PUBLIC_CHAT:
            return await func(update, context)
        
        return
    return wrapper
