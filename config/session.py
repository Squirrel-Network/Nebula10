#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import collections

from expiringdict import ExpiringDict
from telegram.ext import ExtBot

from config import Config
from core.utilities.lang import Lang


class Session:
    bot: ExtBot
    config: Config
    lang: dict[str, Lang]
    owner_ids: list[int]
    antiflood: ExpiringDict[str, int] = ExpiringDict(1000, 11)
    antistorm: ExpiringDict[str, int] = ExpiringDict(1000, 11)
    status: collections.defaultdict[str, dict] = collections.defaultdict(dict)
