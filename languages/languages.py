#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import json
import pathlib

from telegram import Update

from config import Session
from core.database.repository.group_language import GroupLanguageRepository
from core.utilities.lang import Lang


def load_languages() -> dict[str, Lang]:
    languages = dict()
    path = pathlib.Path(__file__).parent

    for x in path.glob("*.json"):
        with open(x, "r") as f:
            languages[x.stem] = json.load(f)

    return languages
    

def get_group_lang(update: Update) -> str | None:
    chat = update.effective_message.chat_id
    row = GroupLanguageRepository().getById([chat])

    if row:
        return row['languages']
    
    return None


def get_lang(update: Update) -> Lang:
    lang = get_group_lang(update)

    if not lang:
        lang = Session.config.DEFAULT_LANGUAGE
    
    return Session.lang[lang.lower()]
