#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class OwnerList(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    tg_username = fields.CharField(50)

    class Meta:
        table = "owner_list"
