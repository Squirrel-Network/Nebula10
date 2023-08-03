#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import re


class Regex:
    HAS_ARABIC: str = "[\u0600-\u06ff]|[\u0750-\u077f]|[\ufb50-\ufbc1]|[\ufbd3-\ufd3f]|[\ufd50-\ufd8f]|[\ufd92-\ufdc7]|[\ufe70-\ufefc]|[\uFDF0-\uFDFD]+"
    HAS_CIRILLIC: str = "[а-яА-Я]+"
    HAS_CHINESE: str = "[\u4e00-\u9fff]+"
    HAS_NUMBER: str = "^[0-9]+$"
    HAS_LETTER: str = "^[a-zA-Z]+$"
    HAS_ZOOPHILE: str = "[ζ]"
    HAS_URL: str = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    HAS_SNAKE_CASE: str = "^[a-z]+(_[a-z]+)*$"

    @classmethod
    def has_arabic_character(cls, data: str) -> bool:
        return bool(re.search(cls.HAS_ARABIC, data))

    @classmethod
    def has_cirillic_character(cls, data: str) -> bool:
        return bool(re.search(cls.HAS_CIRILLIC, data))

    @classmethod
    def has_chinese_character(cls, data: str) -> bool:
        return bool(re.search(cls.HAS_CHINESE, data))

    @classmethod
    def has_zoophile(cls, data: str) -> bool:
        return bool(re.search(cls.HAS_ZOOPHILE, data))

    @classmethod
    def is_snake_case(cls, data: str) -> bool:
        return bool(re.search(cls.HAS_SNAKE_CASE, data))

    @classmethod
    def is_url(cls, data: str) -> bool:
        return bool(re.search(cls.HAS_URL, data))
