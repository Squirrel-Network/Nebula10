#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class SuperbanTable(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    user_first_name = fields.CharField(255, default="Unknown")
    motivation_text = fields.CharField(255)
    user_date = fields.DatetimeField()
    id_operator = fields.BigIntField()
    username_operator = fields.CharField(32)
    first_name_operator = fields.CharField(255)

    class Meta:
        table = "superban_table"
