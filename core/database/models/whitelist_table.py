#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class WhitelistTable(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField()
    tg_username = fields.CharField(32)

    class Meta:
        table = "whitelist_table"
