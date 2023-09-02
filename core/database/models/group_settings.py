#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupSettings(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    set_welcome = fields.BooleanField(default=True)
    set_silence = fields.BooleanField(default=False)
    block_new_member = fields.BooleanField(default=False)
    set_antiflood = fields.BooleanField(default=True)
    set_antistorm = fields.BooleanField(default=False)
    set_user_profile_picture = fields.BooleanField(default=False)
    set_arabic_filter = fields.BooleanField(default=True)
    set_cirillic_filter = fields.BooleanField(default=True)
    set_chinese_filter = fields.BooleanField(default=True)
    zoophile_filter = fields.BooleanField(default=True)
    set_no_vocal = fields.BooleanField(default=False)
    sender_chat_block = fields.BooleanField(default=True)
    spoiler_block = fields.BooleanField(default=False)
    set_captcha = fields.BooleanField(default=False)

    async def get_settings(self):
        return {
            "set_welcome": self.set_welcome,
            "set_silence": self.set_silence,
            "block_new_member": self.block_new_member,
            "set_antiflood": self.set_antiflood,
            "set_user_profile_picture": self.set_user_profile_picture,
            "set_arabic_filter": self.set_arabic_filter,
            "set_cirillic_filter": self.set_cirillic_filter,
            "set_chinese_filter": self.set_chinese_filter,
            "zoophile_filter": self.zoophile_filter,
            "set_no_vocal": self.set_no_vocal,
            "sender_chat_block": self.sender_chat_block,
            "spoiler_block": self.spoiler_block,
            "set_captcha": self.set_captcha,
        }

    async def get_chat_block(self):
        return {
            "block_new_member": self.block_new_member,
            "set_user_profile_picture": self.set_user_profile_picture,
            "set_arabic_filter": self.set_arabic_filter,
            "set_cirillic_filter": self.set_cirillic_filter,
            "set_chinese_filter": self.set_chinese_filter,
            "zoophile_filter": self.zoophile_filter,
        }

    class Meta:
        table = "group_settings"
