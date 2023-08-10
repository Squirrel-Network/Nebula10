#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import ChatPermissions, constants

# general constants
DEFAULT_COUNT_WARN = 0
DEFAULT_USER_SCORE = 0
DEFAULT_MAX_WARN = 3
SERVICE_ACCOUNT = constants.ChatID.SERVICE_CHAT
SUPERGROUP = constants.ChatType.SUPERGROUP
GROUP = constants.ChatType.GROUP
CHANNEL = constants.ChatType.CHANNEL

# constants for time management
# DAILY == 24h  ; TWELVE_HOUR == 12h ; EIGHT_HOUR == 8h ; FOUR_HOUR == 4h ; ONE_HOUR == 1h
DAILY = 86400.0
TWELVE_HOUR = 43200.0
EIGHT_HOUR = 28800.0
FOUR_HOUR = 14400.0
ONE_HOUR = 3600.0
ONE_MINUTE = 60.0

# these constants change and disrupt an entire group
PERM_FALSE = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)

PERM_TRUE = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)

PERM_ALL_TRUE = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=True,
    can_invite_users=True,
    can_pin_messages=True,
    can_manage_topics=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
)

PERM_MEDIA_TRUE = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)

PERM_MEDIA_FALSE = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=False,
    can_send_polls=True,
    can_send_other_messages=False,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)

# Settings Buttons Menu
BUTTONS_MENU = {
    "settings|set_welcome": ("Welcome 👋🏻", "set_welcome"),
    "settings|set_silence": ("Silence 🤫", "set_silence"),
    "settings|set_block_entry": ("Deny All Entry 🚷", "block_new_member"),
    "settings|set_antiflood": ("AntiFlood 🚫", "set_antiflood"),
    "settings|user_photo": (
        "No User Photo Entry ⛔️",
        "set_user_profile_picture",
    ),
    "settings|arabic": ("No Arabic Entry ⛔️", "set_arabic_filter"),
    "settings|cirillic": ("No Russian Entry ⛔️", "set_cirillic_filter"),
    "settings|chinese": ("No Chinese Entry ⛔️", "set_chinese_filter"),
    "settings|zoophile": ("No ZooPhile Entry ⛔️", "zoophile_filter"),
    "settings|novocal": ("Block Vocal ⛔️", "set_no_vocal"),
    "settings|channel_block": ("Block Channel 📢", "sender_chat_block"),
    "settings|spoiler_block": ("Block Spoiler 🚫", "spoiler_block"),
    "settings|set_captcha": ("Captcha", "set_captcha"),
}

# Custom button welcome
CUSTOM_BUTTONS_WELCOME = {"rules": "rules|open"}
