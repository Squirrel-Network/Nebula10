#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class Groups(Model):
    id = fields.IntField(pk=True)
    id_group = fields.BigIntField(unique=True)
    group_name = fields.CharField(255)
    welcome_text = fields.TextField()
    rules_text = fields.TextField()
    community = fields.BooleanField(default=False)
    languages = fields.CharField(3)
    max_warn = fields.IntField(default=3)
    set_cas_ban = fields.BooleanField(default=True)
    type_no_username = fields.IntField(default=1)
    log_channel = fields.BigIntField()
    group_photo = fields.CharField(
        255,
        default="https://nebula.squirrel-network.online/static/group_photo/default.jpg",
    )
    total_users = fields.IntField(default=0)
    ban_message = fields.TextField(
        default="{mention} has been <b>banned</b> from: {chat}"
    )
    antiflood_max_messages = fields.IntField(default=3)
    antiflood_seconds = fields.IntField(default=1)
    antistorm_max_users = fields.IntField(default=15)
    antistorm_seconds = fields.IntField(default=3)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "groups"
