#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import pymysql
from sqlalchemy import create_engine

from config import Session


class Connection:
    """
    This class handles database connection and inbound queries
    """
    
    def __init__(self):
        self.con = pymysql.connect(
            host = Session.config.HOST,
            port = Session.config.PORT,
            user = Session.config.USER,
            password = Session.config.PASSWORD,
            db = Session.config.DBNAME,
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
        self.server = '{}:{}'.format(Session.config.HOST, Session.config.PORT)
        self.db = Session.config.DBNAME
        self.login = Session.config.USER
        self.passwd = Session.config.PASSWORD
        self.engine_str = 'mysql+pymysql://{}:{}@{}/{}'.format(self.login, self.passwd, self.server, self.db)
        self.engine = create_engine(self.engine_str)