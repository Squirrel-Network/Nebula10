#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from typing import Callable, Optional, Pattern, TypeVar, Union

from telegram import Update
from telegram.ext import CallbackQueryHandler as BackCallbackQueryHandler
from telegram.ext import filters as filters_module
from telegram.ext._utils.types import CCT, HandlerCallback

from core.utilities.custom_filters import ALL_CALLBACK_QUERY, CallbackQueryFilter

RT = TypeVar("RT")


class CallbackQueryHandler(BackCallbackQueryHandler):
    __slots__ = ("pattern", "filters")

    def __init__(
        self,
        callback: HandlerCallback[Update, CCT, RT],
        pattern: Union[str, Pattern[str], type, Callable[[object], Optional[bool]]],
        filters: filters_module.BaseFilter = None,
    ) -> None:
        super().__init__(callback, pattern)

        self.filters = filters if filters is not None else ALL_CALLBACK_QUERY

        if not isinstance(self.filters, CallbackQueryFilter):
            raise TypeError(
                "The `filters` must not be an instance of ~core.utilities.custom_filters.CallbackQueryFilter~"
            )

    def check_update(self, update: Update) -> Optional[Union[bool, object]]:
        return super().check_update(update) and self.filters.check_update(update)
