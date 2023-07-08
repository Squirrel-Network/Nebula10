#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Message
from telegram.ext.filters import MessageFilter


class _ReplyText(MessageFilter):
    __slots__ = ()

    def filter(self, message: Message) -> bool:
        return bool(message.reply_to_message.text)


REPLY_TEXT = _ReplyText(name="filters.REPLY_TEXT")
