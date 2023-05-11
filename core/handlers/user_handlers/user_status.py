#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork


async def status(update, context):
    test = update.effective_user
    print("NEW_USER: {}".format(test))
    user = update.effective_message.from_user
    print("USER:\n {}".format(user))
