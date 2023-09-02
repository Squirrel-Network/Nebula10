#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import collections
import typing

from expiringdict import ExpiringDict
from telegram.ext import ExtBot

from config import Config

if typing.TYPE_CHECKING:
    from languages.lang import Lang, LangKeyboard


class Session:
    bot: ExtBot
    config: Config
    lang: dict[str, "Lang"] = {}
    lang_keyboard: dict[str, "LangKeyboard"] = {}
    owner_ids: list[int]
    antiflood: ExpiringDict[str, int] = ExpiringDict(1000, 11)
    antistorm: ExpiringDict[str, int] = ExpiringDict(1000, 11)
    status: collections.defaultdict[str, dict] = collections.defaultdict(dict)
    captcha: collections.defaultdict[str, dict] = collections.defaultdict(dict)
    last_settings: collections.defaultdict[int, int] = collections.defaultdict(int)
