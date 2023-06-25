#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import re

from tortoise import Tortoise

from config import Session
from core.database import models
from core.utilities.regex import Regex


async def init_db():
    conf = Session.config

    await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": conf.HOST,
                        "port": conf.PORT,
                        "user": conf.USER,
                        "password": conf.PASSWORD,
                        "database": conf.DBNAME,
                    },
                }
            },
            "apps": {
                "models": {
                    "models": list(
                        map(
                            lambda x: f"core.database.models.{x}",
                            filter(lambda x: Regex.is_snake_case(x), dir(models)),
                        )
                    ),
                    "default_connection": "default",
                }
            },
            "timezone": "Europe/Rome",
        }
    )
    await Tortoise.generate_schemas()
