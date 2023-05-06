#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import pymysql
from pymysqlpool import ConnectionPool

from config import Session


def create_pool() -> ConnectionPool:
    return ConnectionPool(
        name="pool",
        host=Session.config.HOST,
        port=Session.config.PORT,
        user=Session.config.USER,
        password=Session.config.PASSWORD,
        database=Session.config.DBNAME,
        autocommit=True,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


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
