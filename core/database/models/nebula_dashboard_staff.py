#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class NebulaDashboardStaff(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    description = fields.CharField(1000)
    contact = fields.CharField(50)
    git = fields.CharField(50)
    photo = fields.CharField(255)

    class Meta:
        table = "nebula_dashboard_staff"
