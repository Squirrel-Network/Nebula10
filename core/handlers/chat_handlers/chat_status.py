#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

async def status(update, context):
    chat = update.effective_chat
    print("CHAT:\n {}".format(chat))