#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupsBlacklist(Model):
    id = fields.IntField(pk=True)
    tg_id_group = fields.BigIntField(unique=True)

    class Meta:
        table = "groups_blacklist"
