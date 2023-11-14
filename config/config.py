#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings, case_sensitive=True):
    # Database settings
    HOST: str = Field("localhost", alias="MYSQL_HOST")
    PORT: int = Field(3306, alias="MYSQL_PORT")
    USER: str = Field("root", alias="MYSQL_USER")
    PASSWORD: str = Field(alias="MYSQL_PASSWORD")
    DBNAME: str = Field(alias="MYSQL_DBNAME")

    # Project settings
    BOT_TOKEN: str = Field(alias="TOKEN")
    DEBUG: bool = False
    DEFAULT_LANGUAGE: str = "EN"
    VERSION: str = "10.1.8"
    VERSION_NAME: str = "Lucario"
    REPO: str = "https://github.com/Squirrel-Network/nebula10"
    MAX_ELEMENTS_PAGE: int = 5

    # Webapp
    WEBAPP_URL: str = "https://webapp.nebula.squirrel-network.online"
    INT_WEBSRV_URL: str = "https://nebula.squirrel-network.online"
    WEBAPP_PORT: int = 4046
    TOKEN_SECRET: str = Field(alias="TOKEN_SECRET")
    JWT_TOKEN_EXPIRES: int = 300

    # Telegram settings
    DEFAULT_WELCOME: str = Field(
        "Welcome {USERNAME} to the {CHAT} group", alias="TG_DEFAULT_WELCOME"
    )
    DEFAULT_RULES: str = Field(
        "https://github.com/Squirrel-Network/GroupRules", alias="TG_DEFAULT_RULES"
    )
    DEFAULT_LOG_CHANNEL: int = Field(alias="TG_DEFAULT_LOG_CHANNEL")
    DEFAULT_STAFF_GROUP: int = Field(alias="TG_DEFAULT_STAFF_GROUP")
    DEFAULT_DEBUG_CHANNEL: int = Field(alias="TG_DEFAULT_DEBUG_CHANNEL")
    OWNER_ID: int = Field(alias="TG_OWNER_ID")
    OWNER_USERNAME: str = Field(alias="TG_OWNER_USERNAME")
    MAX_KEYBOARD_ROW: int = 8
    MAX_KEYBOARD_COLUMN: int = 4
    DEVELOPERS_CHAT_ID: list[int] = [1065189838, 1639391463]
