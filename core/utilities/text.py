#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.utilities import emoji


class Text(dict):
    def __getitem__(self, key: str) -> str:
        if value := self.get(key.lower(), None):
            return value

        return getattr(emoji, key, f"{{{key}}}")
