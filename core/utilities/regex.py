#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import re

class Regex(object):
    def __init__(self):
        self.HAS_ARABIC = "[\u0600-\u06ff]|[\u0750-\u077f]|[\ufb50-\ufbc1]|[\ufbd3-\ufd3f]|[\ufd50-\ufd8f]|[\ufd92-\ufdc7]|[\ufe70-\ufefc]|[\uFDF0-\uFDFD]+"
        self.HAS_CIRILLIC = "[а-яА-Я]+"
        self.HAS_CHINESE = "[\u4e00-\u9fff]+"
        self.HAS_NUMBER = "^[0-9]+$"
        self.HAS_LETTER = "^[a-zA-Z]+$"
        self.HAS_ZOOPHILE = "[ζ]"
        self.HAS_URL = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"


    def has_arabic_character(self,string):
        arabic = re.search(self.HAS_ARABIC, string)
        return not not arabic

    def has_cirillic_character(self,string):
        cirillic = re.search(self.HAS_CIRILLIC, string)
        return not not cirillic

    def has_chinese_character(self,string):
        chinese = re.search(self.HAS_CHINESE, string)
        return not not chinese

    def has_zoophile(self,string):
        zoophile = re.search(self.HAS_ZOOPHILE, string)
        return not not zoophile
    def regex_search(self,regex_type,string):
        check = re.search(regex_type, string)
        if check is None:
            return False
        else:
            return True