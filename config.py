#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    ###########################
    ##   DATABASE SETTINGS  ##
    ##########################
    HOST = os.environ.get('MYSQL_HOST', 'localhost')
    PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    USER = os.environ.get('MYSQL_USER', 'root')
    PASSWORD = os.environ.get('MYSQL_PASSWORD')
    DBNAME = os.environ.get('MYSQL_DBNAME')
    BOT_TOKEN = os.environ.get('TOKEN')