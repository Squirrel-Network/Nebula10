#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.utilities import emoji


class Text(dict):
    def __missing__(self, key: str) -> str:
        value = self.get(key.lower(), None)

        if value:
            return value
        elif key in dir(emoji):
            return getattr(emoji, key)
        
        return f"{{{key}}}"
