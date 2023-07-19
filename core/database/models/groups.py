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
    welcome_buttons = fields.TextField(
        default='{"buttons": [{"id": 0, "title": "Bot Logs", "url": "https://t.me/nebulalogs"}]}'
    )
    rules_text = fields.TextField()
    community = fields.BooleanField(default=False)
    languages = fields.CharField(3)
    set_welcome = fields.BooleanField(default=True)
    max_warn = fields.IntField(default=3)
    set_silence = fields.BooleanField(default=False)
    exe_filter = fields.BooleanField(default=False)
    block_new_member = fields.BooleanField(default=False)
    set_arabic_filter = fields.BooleanField(default=True)
    set_cirillic_filter = fields.BooleanField(default=True)
    set_chinese_filter = fields.BooleanField(default=True)
    set_user_profile_picture = fields.BooleanField(default=False)
    gif_filter = fields.BooleanField(default=False)
    set_cas_ban = fields.BooleanField(default=True)
    type_no_username = fields.IntField(default=1)
    log_channel = fields.BigIntField()
    group_photo = fields.CharField(
        255, default="https://naos.hersel.it/group_photo/default.jpg"
    )
    total_users = fields.IntField(default=0)
    zip_filter = fields.BooleanField(default=False)
    targz_filter = fields.BooleanField(default=False)
    jpg_filter = fields.BooleanField(default=False)
    docx_filter = fields.BooleanField(default=False)
    apk_filter = fields.BooleanField(default=False)
    zoophile_filter = fields.BooleanField(default=True)
    sender_chat_block = fields.BooleanField(default=True)
    spoiler_block = fields.BooleanField(default=False)
    set_no_vocal = fields.BooleanField(default=False)
    set_antiflood = fields.BooleanField(default=True)
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
