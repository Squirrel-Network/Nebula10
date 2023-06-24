#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    tg_username = fields.CharField(50)
    created_at = fields.DatetimeField()
    updated_at = fields.DatetimeField()

    class Meta:
        table = "users"
