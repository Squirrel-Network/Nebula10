#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.repository.user import UserRepository
from languages.getlang import languages

def get_owner_list() -> list:
    rows = UserRepository().getOwners()
    arr_owners = []
    for a in rows:
        owners = int(a['tg_id'])
        arr_owners.append(owners)
    return arr_owners

async def close_menu(update, context):
    query = update.callback_query
    languages(update,context)
    if query.data == 'closeMenu':
        await query.message.delete()


