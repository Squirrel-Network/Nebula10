#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseSettings


LIST_ENV = (
    ("HOST", "MYSQL_HOST"),
    ("PORT", "MYSQL_PORT"),
    ("USER", "MYSQL_USER"),
    ("PASSWORD", "MYSQL_PASSWORD"),
    ("DBNAME", "MYSQL_DBNAME"),
    ("BOT_TOKEN", "TOKEN"),
    ("DEFAULT_WELCOME", "TG_DEFAULT_WELCOME"),
    ("DEFAULT_RULES", "TG_DEFAULT_RULES"),
    ("DEFAULT_LOG_CHANNEL", "TG_DEFAULT_LOG_CHANNEL"),
    ("DEFAULT_STAFF_GROUP", "TG_DEFAULT_STAFF_GROUP"),
)


class Config(BaseSettings):
    ###########################
    ##   DATABASE SETTINGS  ##
    ##########################
    HOST: str = "localhost"
    PORT: int = 3306
    USER: str = "root"
    PASSWORD: str
    DBNAME: str
    BOT_TOKEN: str
    ##########################
    ##   PROJECT SETTINGS   ##
    ##########################
    DEBUG: bool = False
    DEFAULT_LANGUAGE: str = "EN"
    VERSION: str = "10.0.0"
    VERSION_NAME: str = "Lucario"
    REPO: str = "https://github.com/Squirrel-Network/nebula10"
    ###########################
    ##   TELEGRAM SETTINGS  ##
    ##########################
    DEFAULT_WELCOME: str = "Welcome {} to the {} group"
    DEFAULT_RULES: str = "https://github.com/Squirrel-Network/GroupRules"
    DEFAULT_LOG_CHANNEL: str
    DEFAULT_STAFF_GROUP: str

    class Config:
        fields = {
            name: {"env": env} 
            for name, env in LIST_ENV
        }