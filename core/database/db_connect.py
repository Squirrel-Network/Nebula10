#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import pymysql
from config import Config
from sqlalchemy import create_engine

"""
This class handles database connection and inbound queries
"""
class Connection:
    def __init__(self):
        self.con = pymysql.connect(
            host = Config.HOST,
            port = Config.PORT,
            user = Config.USER,
            password = Config.PASSWORD,
            db = Config.DBNAME,
            autocommit=True,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
            )
        self.cur = self.con.cursor()

    def _select(self,sql,args=None):
        self.cur.execute(sql,args)
        self.sel = self.cur.fetchone()
        self.cur.close()
        self.con.close()
        return self.sel

    def _selectAll(self,sql,args=None):
        self.cur.execute(sql,args)
        self.sel = self.cur.fetchall()
        self.cur.close()
        self.con.close()
        return self.sel

    def _insert(self,sql,args=None):
        self.ins = self.cur.executemany(sql,args)
        return self.ins

    def _single_insert(self,sql,args=None):
        self.sins = self.cur.execute(sql,args)
        return self.sins

    def _dict_insert(self, sql, dictionary):
        self.dins = self.cur.execute(sql, list(dictionary.values()))
        return self.dins

    def _update(self,sql, args=None):
        self.upd = self.cur.executemany(sql,args)
        return self.upd

    def _delete(self, sql, args=None):
        self.delete = self.cur.executemany(sql,args)
        return self.delete


class SqlAlchemyConnection:
    def __init__(self):
        self.server = '{}:{}'.format(Config.HOST,Config.PORT)
        self.db = Config.DBNAME
        self.login = Config.USER
        self.passwd = Config.PASSWORD
        self.engine_str = 'mysql+pymysql://{}:{}@{}/{}'.format(self.login, self.passwd, self.server, self.db)
        self.engine = create_engine(self.engine_str)