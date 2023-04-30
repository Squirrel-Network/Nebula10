#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from config import Config
from core.utilities.lang import Lang


class Session:
    config: Config
    lang: dict[str, Lang]
