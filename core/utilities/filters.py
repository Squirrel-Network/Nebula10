#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Update, constants
from telegram.ext import ContextTypes

from config import Session
from core.utilities.enums import Role


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


class _All(Filter):
    async def __call__(self, _: Update, __: ContextTypes.DEFAULT_TYPE) -> bool:
        return True


all = _All()


class _Group(Filter):
    async def __call__(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> bool:
        return bool(
            update.effective_chat
            and update.effective_chat.type
            in (constants.ChatType.GROUP, constants.ChatType.SUPERGROUP)
        )


group = _Group()


class _Private(Filter):
    async def __call__(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> bool:
        return bool(
            update.effective_chat
            and update.effective_chat.type == constants.ChatType.PRIVATE
        )


private = _Private()


class _Reply(Filter):
    async def __call__(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> bool:
        return bool(
            update.effective_message and update.effective_message.reply_to_message
        )


reply = _Reply()


class _ReplyText(Filter):
    def filter(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> bool:
        return bool(
            update.effective_message
            and update.effective_message.reply_to_message
            and update.effective_message.reply_to_message.text
        )


reply_text = _ReplyText()


class command(Filter):
    def __init__(self, prefix: list[str]) -> None:
        self.prefix = prefix

    async def __call__(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> bool:
        text = update.effective_message.text

        if not text:
            return False

        return any(map(lambda x: f"/{x}" == text, self.prefix))


class check_role(Filter):
    def __init__(self, *roles: Role) -> None:
        self.roles = roles

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        if not update.effective_chat or not update.effective_user:
            return False

        user = await update.effective_chat.get_member(update.effective_user.id)

        if user.status in self.roles:
            return True
        elif Role.OWNER in self.roles and update.effective_user.id in Session.owner_ids:
            return True

        return False
