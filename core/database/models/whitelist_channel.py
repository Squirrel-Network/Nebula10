#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class WhitelistChannel(Model):
    id = fields.IntField(pk=True)
    tg_channel_id = fields.BigIntField()
    tg_group_id = fields.BigIntField()

    class Meta:
        table = "whitelist_channel"
