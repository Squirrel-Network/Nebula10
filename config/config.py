#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import os
import typing

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)

LIST_ENV = {
    "HOST": "MYSQL_HOST",
    "PORT": "MYSQL_PORT",
    "USER": "MYSQL_USER",
    "PASSWORD": "MYSQL_PASSWORD",
    "DBNAME": "MYSQL_DBNAME",
    "BOT_TOKEN": "TOKEN",
    "TOKEN_SECRET": "TOKEN_SECRET",
    "DEFAULT_WELCOME": "TG_DEFAULT_WELCOME",
    "DEFAULT_RULES": "TG_DEFAULT_RULES",
    "DEFAULT_LOG_CHANNEL": "TG_DEFAULT_LOG_CHANNEL",
    "DEFAULT_STAFF_GROUP": "TG_DEFAULT_STAFF_GROUP",
    "DEFAULT_DEBUG_CHANNEL": "TG_DEFAULT_DEBUG_CHANNEL",
    "OWNER_ID": "TG_OWNER_ID",
    "OWNER_USERNAME": "TG_OWNER_USERNAME",
}


class MyCustomSource(EnvSettingsSource):
    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: typing.Any,
        value_is_complex: bool,
    ) -> typing.Any:
        if v := os.environ.get(LIST_ENV.get(field_name) or ""):
            return v
        return value


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
    DEFAULT_WELCOME: str = "Welcome {USERNAME} to the {CHAT} group"
    DEFAULT_RULES: str = "https://github.com/Squirrel-Network/GroupRules"
    DEFAULT_LOG_CHANNEL: int
    DEFAULT_STAFF_GROUP: int
    DEFAULT_DEBUG_CHANNEL: int
    OWNER_ID: int
    OWNER_USERNAME: str
    MAX_KEYBOARD_ROW: int = 8
    MAX_KEYBOARD_COLUMN: int = 4
    DEVELOPERS_CHAT_ID: list[int] = [1065189838, 1639391463]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)
