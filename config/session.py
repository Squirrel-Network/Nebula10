#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pymysqlpool import ConnectionPool

from config import Config
from core.utilities.lang import Lang


class Session:
    config: Config
    db_pool: ConnectionPool
    lang: dict[str, Lang]
    owner_ids: list[int]
