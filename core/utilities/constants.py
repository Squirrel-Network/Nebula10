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

# Constants for captcha and status management
MAX_TIME_STATUS_CLEANUP = 3 * 60
MAX_TIME_CAPTCHA_CLEANUP = 2.5 * 60

# these constants change and disrupt an entire group
PERM_FALSE = ChatPermissions(
    can_send_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
)

PERM_TRUE = ChatPermissions(
    can_send_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
)

PERM_ALL_TRUE = ChatPermissions(
    can_send_messages=True,
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
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
)

PERM_MEDIA_FALSE = ChatPermissions(
    can_send_messages=True,
    can_send_polls=True,
    can_send_other_messages=False,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
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
        ("SETTINGS_FILTERS", "settings|filters"),
        ("SETTINGS_CHAT_BLOCK", "settings|chat_block"),
    ),
    (
        ("SETTINGS_NIGHT", "settings|night"),
        ("SETTINGS_CAPTCHA", "settings|captcha"),
    ),
)

# Custom button welcome
CUSTOM_BUTTONS_WELCOME = {"rules": "rules|open"}
