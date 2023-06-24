#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.decorators import on_update
from core.utilities.telegram_update import TelegramUpdate


@on_update
async def status(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    test = update.effective_user
    print("NEW_USER: {}".format(test))
    user = update.effective_message.from_user
    print("USER:\n {}".format(user))
