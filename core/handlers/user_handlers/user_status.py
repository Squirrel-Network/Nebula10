#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

async def status(update, context):
    user = update.effective_message.from_user
    print("USER:\n {}".format(user))