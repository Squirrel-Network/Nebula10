#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Message, Update
from telegram.ext import ContextTypes
from telegram.ext.filters import MessageFilter


class Filter:
    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        x = await self.base(update, context)

        return not x


class AndFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        x = await self.base(update, context)
        y = await self.other(update, context)

        return x and y


class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        x = await self.base(update, context)
        y = await self.other(update, context)

        return x or y


class command(Filter):
    def __init__(self, prefix: list[str]) -> None:
        self.prefix = prefix

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        text = update.effective_message.text

        if not text:
            return False

        return any(map(lambda x: x == text, self.prefix))


class _All(Filter):
    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return True


ALL = _All()


class _ReplyText(MessageFilter):
    __slots__ = ()

    def filter(self, message: Message) -> bool:
        return bool(message.reply_to_message.text)


REPLY_TEXT = _ReplyText(name="filters.REPLY_TEXT")
