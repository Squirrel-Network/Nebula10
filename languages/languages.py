#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import json
import pathlib

from telegram import Update

from config import Session
from core.database.models import Groups
from core.utilities.lang import Lang


def load_languages() -> dict[str, Lang]:
    languages = dict()
    path = pathlib.Path(__file__).parent

    for x in path.glob("*.json"):
        with open(x, "r") as f:
            languages[x.stem] = json.load(f)

    return languages


async def get_group_lang(update: Update) -> str | None:
    chat = update.effective_message.chat_id

    data = await Groups.get_or_none(id_group=chat)

    if data:
        return data.languages


async def get_lang(update: Update) -> Lang:
    lang = Session.config.DEFAULT_LANGUAGE

    if (
        update.effective_chat.type == "private"
        and update.effective_user.language_code in ("it", "en")
    ):
        lang = update.effective_user.language_code

    else:
        lang = await get_group_lang(update) or lang

    return Session.lang[lang.lower()]
