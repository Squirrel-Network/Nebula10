#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from collections import defaultdict

from config import Config
from core.utilities.lang import Lang


class Session:
    config: Config
    lang: dict[str, Lang]
    owner_ids: list[int]
    antiflood: defaultdict[int, defaultdict[int, list]] = defaultdict(
        lambda: defaultdict(list)
    )
