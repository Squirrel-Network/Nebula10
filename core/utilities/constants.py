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

# Allowed HTML Tags
ALLOWED_HTML_TAGS = (
    "b",
    "strong",
    "i",
    "em",
    "u",
    "ins",
    "s",
    "strike",
    "del",
    "span",
    "tg-spoiler",
    "a",
    "tg-emoji",
    "code",
    "pre",
)

# Settings Buttons Menu
BUTTONS_SETTINGS = {
    "set_welcome": "Welcome 👋🏻",
    "set_silence": "Silence 🤫",
    "block_new_member": "Deny All Entry 🚷",
    "set_antiflood": "AntiFlood 🚫",
    "set_user_profile_picture": "No User Photo Entry ⛔️",
    "set_arabic_filter": "No Arabic Entry ⛔️",
    "set_cirillic_filter": "No Russian Entry ⛔️",
    "set_chinese_filter": "No Chinese Entry ⛔️",
    "zoophile_filter": "No ZooPhile Entry ⛔️",
    "set_no_vocal": "Block Vocal ⛔️",
    "sender_chat_block": "Block Channel 📢",
    "spoiler_block": "Block Spoiler 🚫",
    "set_captcha": "Captcha",
}

SETTING_BUTTONS = (
    (
        ("SETTINGS_WELCOME", "settings|welcome"),
        ("SETTINGS_RULES", "settings|rules"),
    ),
    (
        ("SETTINGS_ANTIFLOOD", "settings|antiflood"),
        ("SETTINGS_ANTISTORM", "settings|antistorm"),
    ),
    (
        ("SETTINGS_NIGHT", "settings|night"),
        ("SETTINGS_CHAT_BLOCK", "settings|chat_block"),
    ),
    (("SETTINGS_CAPTCHA", "settings|captcha"),),
)

# Custom button welcome
CUSTOM_BUTTONS_WELCOME = {"rules": "rules|open"}
