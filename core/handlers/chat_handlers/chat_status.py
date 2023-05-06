#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork


async def status(update, context):
    chat = update.effective_chat
    msg_update = update.effective_message
    group_members_count = await chat.get_member_count()

    # Update Title
    if msg_update.new_chat_title:
        print(
            "LA CHAT HA CAMBIATO TITOLO\nIL NUOVO TITOLO: {}".format(
                msg_update.new_chat_title
            )
        )

    # Update Members Count
    if group_members_count > 0:
        print(group_members_count)

    print("CHAT:\n {}".format(chat))
