#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from expiringdict import ExpiringDict

from config import Config
from core.utilities.lang import Lang


class Session:
    config: Config
    lang: dict[str, Lang]
    owner_ids: list[int]
    antiflood: ExpiringDict[str, int] = ExpiringDict(10000, 11)
