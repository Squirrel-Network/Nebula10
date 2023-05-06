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
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
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
        self.con.close()

    def _select(self, sql, args=None):
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchone()

    def _selectAll(self, sql, args=None):
        with self.con.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchall()

    def _insert(self, sql, args=None):
        with self.con.cursor() as cursor:
            return cursor.executemany(sql, args)

    def _single_insert(self, sql, args=None):
        with self.con.cursor() as cursor:
            return cursor.execute(sql, args)

    def _dict_insert(self, sql, dictionary):
        with self.con.cursor() as cursor:
            return cursor.execute(sql, list(dictionary.values()))

    def _update(self, sql, args=None):
        with self.con.cursor() as cursor:
            return cursor.executemany(sql, args)

    def _delete(self, sql, args=None):
        with self.con.cursor() as cursor:
            return cursor.executemany(sql, args)
