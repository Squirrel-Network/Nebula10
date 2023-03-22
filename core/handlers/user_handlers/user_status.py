#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.utilities.entities import TelegramObjects
async def status(update, context):
    test = TelegramObjects(update,context).new_user_object()
    print("NEW_USER: {}".format(test))
    user = update.effective_message.from_user
    print("USER:\n {}".format(user))