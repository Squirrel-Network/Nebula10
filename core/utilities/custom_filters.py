#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from abc import abstractmethod

from telegram import CallbackQuery, Update
from telegram.ext.filters import BaseFilter


class CallbackQueryFilter(BaseFilter):
    def check_update(self, update: Update) -> bool:
        if update.callback_query:
            return self.filter(update.callback_query)
        return False

    @abstractmethod
    def filter(self, callback_query: CallbackQuery) -> bool:
        ...


class _AllCallbackQuery(CallbackQueryFilter):
    __slots__ = ()

    def filter(self, _: CallbackQuery) -> bool:
        return True


ALL_CALLBACK_QUERY = _AllCallbackQuery(name="filters.ALL_CALLBACK_QUERY")
