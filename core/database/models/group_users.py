#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupUsers(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField()
    tg_group_id = fields.BigIntField()
    warn_count = fields.IntField(default=0)
    user_score = fields.BigIntField(default=0)

    class Meta:
        table = "group_users"
        unique_together = [("tg_id", "tg_group_id")]
