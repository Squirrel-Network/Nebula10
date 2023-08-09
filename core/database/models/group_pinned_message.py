#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupPinnedMessage(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "group_pinned_message"
        unique_together = [("chat_id", "message_id")]
