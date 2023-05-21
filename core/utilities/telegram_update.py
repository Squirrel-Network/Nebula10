#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import dataclasses

from telegram import Update, Chat, User


@dataclasses.dataclass
class TelegramUpdate:
    update: Update
    chat: Chat | None
    user: User | None
    user_reply: User | None
