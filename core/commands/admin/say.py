#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.decorators import check_role, delete_command
from core.utilities.enums import Role
from core.utilities.message import message
from languages import get_lang


@check_role(Role.OWNER, Role.CREATOR, Role.ADMINISTRATOR)
@delete_command
async def init(update,context):
    msg = update.message.text[4:].strip()
    
    if msg != "":
        await message(update, context, msg, 'HTML', 'message', None, None)
    else:
        await message(update, context, get_lang(update)["SAY_MESSAGE"], 'HTML', 'message', None, None)
