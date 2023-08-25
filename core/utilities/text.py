#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import html
import re

from core.utilities import emoji


class Text(dict):
    def __getitem__(self, key: str) -> str:
        if (value := self.get(key.lower(), None)) is not None:
            return re.sub(r"<>(.*?)</>", lambda x: html.escape(x.group(1)), str(value))

        return getattr(emoji, key, f"{{{key}}}")
