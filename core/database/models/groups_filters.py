#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupsFilters(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    exe_filter = fields.BooleanField(default=False)
    gif_filter = fields.BooleanField(default=False)
    jpg_filter = fields.BooleanField(default=False)
    docx_filter = fields.BooleanField(default=False)
    apk_filter = fields.BooleanField(default=False)
    compress_filter = fields.BooleanField(default=False)

    class Meta:
        table = "groups_filters"
