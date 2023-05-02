#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.decorators import restricted
from core.utilities.message import message
from languages import get_lang


async def init(update,context):
    msg = update.message.text[4:].strip()
    
    if msg != "":
        await message(update, context, msg, 'HTML', 'message', None, None)
    else:
        await message(update, context, get_lang(update)["SAY_MESSAGE"], 'HTML', 'message', None, None)
