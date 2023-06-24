#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupsBadwords(Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(255)
    tg_group_id = fields.BigIntField()

    class Meta:
        table = "groups_badwords"
