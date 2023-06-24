#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import re

from tortoise import Tortoise

from config import Session
from core.database import models


def is_snake_case(string):
    pattern = r"^[a-z]+(_[a-z]+)*$"
    return bool(re.match(pattern, string))


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
                            filter(lambda x: is_snake_case(x), dir(models)),
                        )
                    ),
                    "default_connection": "default",
                }
            },
            "timezone": "Europe/Rome",
        }
    )
    await Tortoise.generate_schemas()


class Connection:
    """
    This class handles database connection and inbound queries
    """

    def __init__(self):
        self.con = Session.db_pool.get_connection()

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        del args
        self.con.close()

    def _select(self, sql: str, args: tuple = None):
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchone()

    def _select_all(self, sql: str, args: tuple = None):
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchall()

    def _execute_many(self, sql: str, args: list[tuple] = None):
        with self.con.cursor() as cursor:
            return cursor.executemany(sql, args)

    def _execute(self, sql: str, args: tuple = None):
        with self.con.cursor() as cursor:
            return cursor.execute(sql, args)

    def _dict_insert(self, sql: str, dictionary: dict):
        with self.con.cursor() as cursor:
            return cursor.execute(sql, list(dictionary.values()))
