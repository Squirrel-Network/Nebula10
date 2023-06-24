#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class NebulaDashboardContent(Model):
    article_id = fields.IntField(pk=True)
    article_title = fields.CharField(55)
    title = fields.CharField(50)
    language = fields.CharField(3)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    author = fields.CharField(50)

    class Meta:
        table = "nebula_dashboard_content"
