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
    ##########################
    ##   PROJECT SETTINGS   ##
    ##########################
    DEBUG = False
    DEFAULT_LANGUAGE = "EN"
    VERSION = '10.0.0'
    VERSION_NAME = 'Lucario'
    REPO = 'https://github.com/Squirrel-Network/nebula10'
    ###########################
    ##   TELEGRAM SETTINGS  ##
    ##########################
    DEFAULT_WELCOME = os.environ.get('TG_DEFAULT_WELCOME', 'Welcome {} to the {} group')
    DEFAULT_RULES = os.environ.get('TG_DEFAULT_RULES', 'https://github.com/Squirrel-Network/GroupRules')
    DEFAULT_LOG_CHANNEL = os.environ.get('TG_DEFAULT_LOG_CHANNEL')
    DEFAULT_STAFF_GROUP = os.environ.get('TG_DEFAULT_STAFF_GROUP')