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
    ("TOKEN_SECRET", "TOKEN_SECRET"),
    ("DEFAULT_WELCOME", "TG_DEFAULT_WELCOME"),
    ("DEFAULT_RULES", "TG_DEFAULT_RULES"),
    ("DEFAULT_LOG_CHANNEL", "TG_DEFAULT_LOG_CHANNEL"),
    ("DEFAULT_STAFF_GROUP", "TG_DEFAULT_STAFF_GROUP"),
    ("OWNER_ID", "TG_OWNER_ID"),
    ("OWNER_USERNAME", "TG_OWNER_USERNAME"),
)


class Config(BaseSettings):
    # Database settings
    HOST: str = "localhost"
    PORT: int = 3306
    USER: str = "root"
    PASSWORD: str
    DBNAME: str
    BOT_TOKEN: str

    # Project settings
    DEBUG: bool = False
    DEFAULT_LANGUAGE: str = "EN"
    VERSION: str = "10.0.0"
    VERSION_NAME: str = "Lucario"
    REPO: str = "https://github.com/Squirrel-Network/nebula10"

    # Webapp
    WEBAPP_URL: str = "https://webapp.nebula.squirrel-network.online"
    INT_WEBSRV_URL: str = "https://nebula.squirrel-network.online"
    WEBAPP_PORT: int = 4046
    TOKEN_SECRET: str
    JWT_TOKEN_EXPIRES: int = 300

    # Telegram settings
    DEFAULT_WELCOME: str = "Welcome {USERNAME} to the {NAME} group"
    DEFAULT_RULES: str = "https://github.com/Squirrel-Network/GroupRules"
    DEFAULT_LOG_CHANNEL: str
    DEFAULT_STAFF_GROUP: str
    OWNER_ID: int
    OWNER_USERNAME: str

    class Config:
        fields = {name: {"env": env} for name, env in LIST_ENV}
