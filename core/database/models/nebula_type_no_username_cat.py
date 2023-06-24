#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class NebulaTypeNoUsernameCat(Model):
    id = fields.IntField(pk=True)
    type_no_username_id = fields.IntField()
    type_no_username_desc = fields.CharField(50)

    class Meta:
        table = "nebula_type_no_username_cat"
