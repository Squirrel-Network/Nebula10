#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.constants import ChatType
from tortoise import fields
from tortoise.models import Model


class Community(Model):
    id = fields.IntField(pk=True)
    tg_group_name = fields.CharField(255)
    tg_group_id = fields.BigIntField(unique=True)
    tg_group_link = fields.TextField()
    type = fields.CharEnumField(ChatType)

    class Meta:
        table = "community"
