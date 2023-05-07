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

    @staticmethod
    def has_arabic_character(data: str) -> bool:
        return bool(re.search(Regex.HAS_ARABIC, data))

    @staticmethod
    def has_cirillic_character(data: str) -> bool:
        return bool(re.search(Regex.HAS_CIRILLIC, data))

    @staticmethod
    def has_chinese_character(string) -> bool:
        return bool(re.search(Regex.HAS_CHINESE, string))

    @staticmethod
    def has_zoophile(data: str) -> bool:
        return bool(re.search(Regex.HAS_ZOOPHILE, data))
