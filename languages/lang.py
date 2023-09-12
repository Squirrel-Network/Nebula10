#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import typing


class SettingsWelcomeTexts(typing.TypedDict):
    SETTINGS_WELCOME: str
    SETTINGS_WELCOME_TEXT: str
    SETTINGS_WELCOME_TEXT_INVALID_HTML: str
    SETTINGS_WELCOME_TEXT_DONE: str


class SettingsChatBlockTexts(typing.TypedDict):
    MAIN_TEXT: str
    BLOCKS_TEXT: str


class SettingsCaptchaTexts(typing.TypedDict):
    MAIN_TEXT: str


class SettingsAntifloodTexts(typing.TypedDict):
    MAIN_TEXT: str


class SettingsAntistormTexts(typing.TypedDict):
    MAIN_TEXT: str


class SettingsTexts(typing.TypedDict):
    SETTINGS_MODE_SELECTION: str
    SETTINGS_MAIN_TEXT: str
    WELCOME: SettingsWelcomeTexts
    CHAT_BLOCK: SettingsChatBlockTexts
    CAPTCHA: SettingsCaptchaTexts
    ANTIFLOOD: SettingsAntifloodTexts
    ANTISTORM: SettingsAntistormTexts


class Lang(typing.TypedDict):
    BLOCK_NEW_MEMBER: str
    BAN_ZOOPHILE: str
    BAN_SELF_BAN: str
    BAN_ERROR_AC: str
    BAN_SUCCESS: str
    BAN_ERROR_SYNTAX: str
    BAN_EMPTY_ERROR: str
    SET_BAN_MESSAGE: str
    BOT_WELCOME: str
    ERROR_MESSAGE_REPLY: str
    FILTERS_COMMAND: str
    FILTER_NAME: str
    HELP_COMMAND: str
    KICKED_USER_MESSAGE_NO_USERNAME: str
    LANG_DEFAULT: str
    LANG_FLAG: str
    LANG_SELECTED: str
    MESSAGE_DM_FILTERS: str
    NEW_MEMBER_WITHOUT_PHOTO: str
    OPERATOR_JOIN: str
    RULES: str
    SAY_MISSING_MESSAGE_WARNING: str
    SELECT_LANG: str
    SERVER_STATUS_CPU: str
    SERVER_STATUS_DISK: str
    SERVER_STATUS_DISK_MESSAGE: str
    SERVER_STATUS_MEMORY: str
    SERVER_STATUS_NETWORK: str
    SERVER_STATUS_SYSTEM: str
    SUPERBAN: str
    SUPERBAN_ALREADY_EXIST: str
    SUPERBAN_ERROR: str
    SUPERBAN_ERROR_ID: str
    SUPERBAN_ERROR_NO_ID: str
    SUPERBAN_ERROR_USERNAME: str
    SUPERBAN_LOG: str
    SUPERBAN_MULTI: str
    SUPERBAN_REMOVE: str
    SUPERBAN_REMOVE_ERROR: str
    SUPERBAN_REPLY: str
    SUPERBAN_WHITELIST: str
    USER_ALREADY_BAN: str
    USER_INFORMATION: str
    USER_INFORMATION_SUPERBAN: str
    UNBAN_SUCCESS: str
    UNBAN_ERROR: str
    START_COMMAND: str
    OWNER_ALREADY_EXIST: str
    OWNER_ADD: str
    OWNER_REMOVE: str
    PERM_MSG_ERROR: str
    PERM_MSG_OK: str
    WARN_USER_REASON: str
    WARN_USER: str
    WARN_DOWN: str
    WARN_DOWN_ERR: str
    WARN_UP: str
    WARN_UP_ERR: str
    WARN_DEL: str
    WARN_USER_MAX: str
    WARN_SETTING: str
    WARN_SETTING_SUCCESS: str
    ANTIFLOOD_SETTING: str
    ANTIFLOOD_ERROR: str
    ANTISTORM_SETTING: str
    AUTOMATIC_HANDLER_USERNAME_KICK: str
    AUTOMATIC_HANDLER_USERNAME_WARNING: str
    AUTOMATIC_HANDLER_USERNAME_MUTE: str
    AUTOMATIC_HANDLER_USERNAME_BAN: str
    AUTOMATIC_HANDLER_NO_PHOTO: str
    AUTOMATIC_HANDLER_SUPERBAN: str
    AUTOMATIC_HANDLER_MAX_WARN: str
    AUTOMATIC_HANDLER_BAD_WORD: str
    AUTOMATIC_HANDLER_SPOILER: str
    AUTOMATIC_HANDLER_CHANNEL: str
    AUTOMATIC_HANDLER_VOICE: str
    SET_WELCOME_ERROR: str
    SET_WELCOME_SUCCESS: str
    SET_RULES_ERROR: str
    SET_RULES_SUCCESS: str
    RULES_MSG: str
    RULES_BUTTON: str
    AUTOMATIC_FILTER_HANDLER_APK: str
    AUTOMATIC_FILTER_HANDLER_DOCX: str
    AUTOMATIC_FILTER_HANDLER_EXE: str
    AUTOMATIC_FILTER_HANDLER_GIF: str
    AUTOMATIC_FILTER_HANDLER_JPG: str
    AUTOMATIC_FILTER_HANDLER_ZIP_TARGZ: str
    SET_WELCOME_BUTTONS: str
    SET_WELCOME_BUTTONS_ADD: str
    SET_WELCOME_BUTTONS_ADD_ERROR: str
    SET_WELCOME_BUTTONS_DEL_CONFIRM: str
    GROUP_STATUS_CLEANUP: str
    MESSAGE_DB_STATUS: str
    STATUS_COMMAND: str
    CHAT_ID_COMMAND: str
    REPORT_ADMIN_MSG: str
    ADD_COMMUNITY_ERROR: str
    ADD_COMMUNITY_UPDATE: str
    ADD_COMMUNITY: str
    FIKO_EGGS: str
    KICK_ME_COMMAND: str
    PIN_COMMAND: str
    UNPIN_COMMAND: str
    UNPIN_COMMAND_ERROR: str
    PINNED_COMMAND: str
    PINNED_COMMAND_ERROR: str
    WELCOME_CAPTCHA: str
    WELCOME_CAPTCHA_ERROR_USER_ID: str
    WELCOME_CAPTCHA_NOT_RESOLVE: str
    WELCOME_CAPTCHA_NOT_VALID: str
    WELCOME_CAPTCHA_CLEANUP: str
    BAN_ERROR_NO_ID: str
    SETTINGS_MODE_SELECTION: str
    SETTINGS_WELCOME: str
    SETTINGS_WELCOME_TEXT: str
    SETTINGS: SettingsTexts


class SettingsMainButtonTexts(typing.TypedDict):
    SETTINGS_WELCOME: str
    SETTINGS_RULES: str
    SETTINGS_ANTIFLOOD: str
    SETTINGS_ANTISTORM: str
    SETTINGS_FILTERS: str
    SETTINGS_CHAT_BLOCK: str
    SETTINGS_NIGHT: str
    SETTINGS_CAPTCHA: str


class WelcomeKeyboardTexts(typing.TypedDict):
    SETTINGS_WELCOME_SET_MESSAGE: str
    SETTINGS_WELCOME_SEE_MESSAGE: str


class ChatBlockBlocksButtonsKeyboardTexts(typing.TypedDict):
    BLOCK_NEW_MEMBER: str
    SET_USER_PROFILE_PICTURE: str
    SET_ARABIC_FILTER: str
    SET_CIRILLIC_FILTER: str
    SET_CHINESE_FILTER: str
    ZOOPHILE_FILTER: str


class ChatBlockKeyboardTexts(typing.TypedDict):
    OBLIGATIONS: str
    BLOCKS: str
    BLOCKS_BUTTONS: ChatBlockBlocksButtonsKeyboardTexts
    ACTIVE_BUTTON: str
    DEACTIVE_BUTTON: str


class SettingsKeyboardTexts(typing.TypedDict):
    MAIN_BUTTON: SettingsMainButtonTexts
    WELCOME: WelcomeKeyboardTexts
    CHAT_BLOCK: ChatBlockKeyboardTexts
    ACTIVE: str
    DEACTIVE: str


class LangKeyboard(typing.TypedDict):
    SETTINGS: SettingsKeyboardTexts
    CLOSE: str
    LANG: str
    BACK: str
    CANCEL: str
