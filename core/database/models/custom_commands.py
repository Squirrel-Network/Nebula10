#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class CustomCommands(Model):
    id = fields.IntField(pk=True)
    tg_group_id = fields.BigIntField(unique=True)
    alias = fields.CharField(50, unique=True)
    command = fields.CharField(50)

    class Meta:
        table = "custom_commands"
