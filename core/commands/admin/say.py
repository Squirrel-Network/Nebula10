#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from core.decorators import restricted
from languages.getLang import languages
from core.utilities.message import message

@restricted.admin
async def init(update,context):
    languages(update,context)
    msg = update.message.text[4:].strip()
    if msg != "":
        await message(update, context, msg, 'HTML', 'message', None, None)
    else:
        await message(update, context, languages.say_error, 'HTML', 'message', None, None)