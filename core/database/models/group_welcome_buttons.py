#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupWelcomeButtons(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()
    row = fields.IntField()
    column = fields.IntField()
    text = fields.TextField()
    url = fields.TextField()

    class Meta:
        table = "group_welcome_buttons"
        unique_together = [("chat_id", "row", "column")]
