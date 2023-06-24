#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class CustomHandler(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    question = fields.CharField(255, unique=True)
    answer = fields.CharField(255)

    class Meta:
        table = "custom_handler"
