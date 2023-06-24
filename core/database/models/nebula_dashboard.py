#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class NebulaDashboard(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField()
    tg_username = fields.CharField(32)
    tg_group_id = fields.BigIntField()
    enable = fields.BooleanField(default=True)
    role = fields.CharField(255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "nebula_dashboard"
